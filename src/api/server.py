import weaviate
import json

from fastapi import FastAPI, status, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
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


class _RAGBody(BaseModel):
    prompt: str


class _WeaviateObjectsResponseBody(BaseModel):
    title: str
    paragraph: str
    sources: list[str]


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
    response = await collection_ba.query.hybrid(query=prompt, limit=limit)

    return [
        _WeaviateObjectsResponseBody(
            title=obj.properties["title"],
            paragraph=obj.properties["paragraph"],
            sources=obj.properties["sources"],
        )
        for obj in response.objects
    ]


@app.post("/generate/", status_code=status.HTTP_200_OK)
async def post_generate_answer(
    body: _RAGBody, limit: int = 2, stream: bool = True, model: str = "llama3.1"
): 
    if not await weaviate_async_client.is_ready():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Weaviate is not ready",
        )

    rag_objects: list[_WeaviateObjectsResponseBody] = await post_near_text(body, limit=limit)

    rag_content = "\n".join([rag_obj.paragraph for rag_obj in rag_objects])
    rag_sources = list(chain(*[rag_obj.sources for rag_obj in rag_objects]))

    prompt = f"You are given this query: {body.model_dump().get("prompt")}. Additional information that you must use to answer the query are provided here: {rag_content}"

    if not stream:
        llm_response = await ollama_async_client.generate(model=model, prompt=prompt, stream=stream)
        return _RAGResponseBody(
            llm_answer=llm_response["response"],
            sources=list(set(rag_sources))
        )
    else:
        llm_response_stream = await ollama_async_client.generate(model=model, prompt=prompt, stream=stream)

        async def encode_response():
            async for item in llm_response_stream:
                if item.get("done"):
                    item.update({"sources": rag_sources})
                yield json.dumps(item)

        return StreamingResponse(encode_response())
