import weaviate
import json

from fastapi import FastAPI, status, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from contextlib import asynccontextmanager
from pydantic import BaseModel
from ollama import AsyncClient
from itertools import chain

from config import collection_name as weaviate_collection


weaviate_async_client = weaviate.use_async_with_local()
ollama_async_client = AsyncClient()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await weaviate_async_client.connect()
    yield
    await weaviate_async_client.close()


app = FastAPI(lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# app.add_middleware(HTTPSRedirectMiddleware)


class _RAGBody(BaseModel):
    prompt: str

class _OllamaBody(BaseModel):
    prompt_user: str
    prompt_system: str

class _WeaviateObjectsResponseBody(BaseModel):
    title: str
    description: str
    source: str
    table: str

class _RAGResponseBody(BaseModel):
    llm_answer: str
    sources: list[str]


@app.post("/neartext/", status_code=status.HTTP_200_OK)
async def post_near_text(
    body: _RAGBody, limit: int = 5
) -> list[_WeaviateObjectsResponseBody]:
    if not await weaviate_async_client.is_ready():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Weaviate is not ready",
        )

    body_json = body.model_dump()

    if not (prompt := body_json.get("prompt")):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Text field is missing"
        )

    collection_ba = weaviate_async_client.collections.get(weaviate_collection)
    response = await collection_ba.query.hybrid(query=prompt, max_vector_distance=0.25, limit=limit)

    return [
        _WeaviateObjectsResponseBody(
            title=title if (title := obj.properties["title"]) else "no title",
            description=description if (description := obj.properties["description"]) else "no description",
            source=source if (source := obj.properties["sources"]) else "no source",
            table=table if (table := obj.properties["table"]) else "no table",
        )
        for obj in response.objects
    ]


@app.post("/generate-rag/", status_code=status.HTTP_200_OK)
async def post_generate_answer(
    body: _RAGBody, limit: int = 2, stream: bool = True, model: str = "llama3.1"
):
    if not await weaviate_async_client.is_ready():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Weaviate is not ready",
        )

    rag_objects: list[_WeaviateObjectsResponseBody] = await post_near_text(
        body, limit=limit
    )

    rag_content = "\n".join([rag_obj.paragraph for rag_obj in rag_objects])
    rag_sources = list(chain(*[rag_obj.sources for rag_obj in rag_objects]))

    prompt = f"You are given this query: {body.model_dump().get("prompt")}. Additional information that you must use to answer the query are provided here: {rag_content}"

    if not stream:
        print("non-stream")
        llm_response = await ollama_async_client.generate(
            model=model, prompt=prompt, stream=stream
        )
        return _RAGResponseBody(
            llm_answer=llm_response["response"], sources=list(set(rag_sources))
        )
    else:
        llm_response_stream = await ollama_async_client.generate(
            model=model, prompt=prompt, stream=stream
        )

        async def encode_response():
            async for item in llm_response_stream:
                if item.get("done"):
                    item.update({"sources": rag_sources})
                yield json.dumps(item)

        return StreamingResponse(encode_response())



@app.post("/generate/", status_code=status.HTTP_200_OK)
async def post_generate_answer(
    body: _OllamaBody, model: str = "llama3.1"
):
    prompt = body.model_dump()
    prompt_user = prompt.get("prompt_user")
    prompt_system = prompt.get("prompt_system")

    print(prompt)

    llm_response = await ollama_async_client.generate(
        model=model, prompt=prompt_user, system=prompt_system, stream=False
    )
    return _RAGResponseBody(
        llm_answer=llm_response["response"], sources=[]
    )
    

@app.get("/")
async def root():
    return {"message": "Hello World"}
