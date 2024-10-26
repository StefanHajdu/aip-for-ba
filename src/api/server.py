import weaviate
import json
import re
import requests
import pandas as pd

from fastapi import FastAPI, status, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from contextlib import asynccontextmanager
from pydantic import BaseModel
from ollama import AsyncClient
from itertools import chain

from config import collection_name as weaviate_collection, system_prompt, pattern_json


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
    response = await collection_ba.query.hybrid(query=prompt, limit=limit)

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
    body: _RAGBody, limit: int = 2, stream: bool = False, model: str = "llama3.1"
):
    if not await weaviate_async_client.is_ready():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Weaviate is not ready",
        )

    rag_objects: list[_WeaviateObjectsResponseBody] = await post_near_text(
        body, limit=limit
    )

    rag_content = "\n".join([' '.join([rag_obj.title, rag_obj.description])  for rag_obj in rag_objects])
    rag_sources = list(chain(*[rag_obj.source for rag_obj in rag_objects]))

    user_prompt = f"You are given this query: {body.model_dump().get("prompt")}. Additional information that you must use to answer the query are provided here: {rag_content}"

    llm_response = await ollama_async_client.generate(
        model=model, prompt=user_prompt, system=system_prompt, stream=stream
    )

    print(f"llm_res: {llm_response["response"]}")

    if "action" in llm_response["response"]:
        # Extract parameters for aggregation
        match = re.search(pattern_json, llm_response["response"], re.DOTALL)
        if match:
            json_str = match.group()
            json_data = json.loads(json_str)
            response_ = await process_data_with_pandas(rag_objects, user_prompt, json_data)
            return _RAGResponseBody(
                llm_answer="Action:" + response_, sources=list(set(rag_sources))
            )
        else:
            print("No valid JSON found in the response.")
            return _RAGResponseBody(
                llm_answer="No valid JSON found in the response", sources=list(set(rag_sources))
            )

    return _RAGResponseBody(
            llm_answer=llm_response["response"], sources=list(set(rag_sources))
        )



@app.post("/generate/", status_code=status.HTTP_200_OK)
async def post_generate_answer(
    body: _OllamaBody, model: str = "llama3.1"
):
    prompt = body.model_dump()
    prompt_user = prompt.get("prompt_user")
    prompt_system = prompt.get("prompt_system")
    llm_response = await ollama_async_client.generate(
        model=model, prompt=prompt_user, system=prompt_system, stream=False
    )
    return _RAGResponseBody(
        llm_answer=llm_response["response"], sources=[]
    )
    

@app.get("/")
async def root():
    return {"message": "Hello World"}


async def process_data_with_pandas(rag_objects, prompt, json_data) -> dict:
    titles = [rag_object.title for rag_object in rag_objects]
    user_prompt_tables = f"Which table is most relevant for query: {prompt}. Table names: {titles}. Return just title of table you recommend no other text."
    llm_response = await ollama_async_client.generate(
        model="llama3.1", prompt=user_prompt_tables, stream=False
    )
    table_name = llm_response["response"].replace('"', "")

    table_url = None
    for i in rag_objects:
        if table_name == i.title:
            table_url = i.table
            break

    def process_data_with_pandas(table_url, json_data) -> dict:
        print(f"table: {table_url}")
        print(f"json_data: {json_data}")
        try:
            table_json = requests.get("https://services8.arcgis.com/pRlN1m0su5BYaFAS/ArcGIS/rest/services/Emisie_z%C3%A1kladn%C3%BDch_zne%C4%8Dis%C5%A5uj%C3%BAcich_l%C3%A1tok_pod%C4%BEa_monitorovac%C3%ADch_stan%C3%ADc_od_roku_2017/FeatureServer/0/query?where=1%3D1&outFields=*&returnGeometry=false&outSR=&f=json")
            rows = [row.get('attributes') for row in table_json.json().get('features')]
        
            df = pd.json_normalize(rows)
            df["Hodnota"] = pd.to_numeric(df["Hodnota"], errors='coerce').astype(float)
            print(f"{df}")
            df_filtered = df[df["Látka"] == "CO**"]
        except Exception as e:
            print(f'No features in {e}')
            return None

        if json_data["action"] == "min":
            result_row = df_filtered.loc[df_filtered["Hodnota"].idxmin()]
        elif json_data["action"] == "max":
            result_row = df_filtered.loc[df_filtered["Hodnota"].idxmax()]
        else:
            raise ValueError("Invalid aggregation action")

        return {
            "monitoring_station": result_row["Monitorovacia_stanica"],
            "year": result_row["Rok"],
            "value": result_row["Hodnota"]
        }

    ret_val = process_data_with_pandas(table_url, json_data)

    print(f"ret_val: {ret_val}")

    question_prompt = f"""
    Question was: {prompt}
    The response that needs to be summarized is in the json. Please, transfer it to one
    answer as a continuous text.
    Response: {ret_val}
    """
    second_iteration_prompt = """
    You are an intelligent assistant. Summarize the response as an answer that will
    be shown to the end user.
    """
    
    response = await post_generate_answer(
        _OllamaBody(
            prompt_user=question_prompt,
            prompt_system=second_iteration_prompt
        )
    )
    print(response)
    return response.llm_answer
