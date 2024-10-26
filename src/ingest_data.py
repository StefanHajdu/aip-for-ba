import json
import weaviate
from weaviate.collections.collection import Collection
from weaviate.classes.config import Configure, Property, DataType, Tokenization, VectorDistances
from weaviate import classes as wvc
from weaviate.util import generate_uuid5

from Translator import Translator
from custom_types import DataObj

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-t", "--translate", action='store_true')
parser.add_argument("-p", "--path")

args = parser.parse_args()
translate = args.translate
path = args.path

collection_name = "bratislava_pages_006"

def ingest_to_weaviate(client: weaviate.WeaviateClient, data: list[DataObj]) -> Collection:
    try:
        created_collection = client.collections.create(
            name=collection_name,
            properties=[
                Property(
                    name="title",
                    data_type=DataType.TEXT,
                    vectorize_property_name=False,
                    tokenization=Tokenization.WORD,
                    index_searchable=True,
                ),
                Property(
                    name="description",
                    data_type=DataType.TEXT,
                    vectorize_property_name=False,
                    tokenization=Tokenization.WORD,
                    index_searchable=True,
                ),
                # disabled indexing for source urls
                Property(
                    name="sources",
                    data_type=DataType.TEXT,
                    vectorize_property_name=False,
                    skip_vectorization=True,
                    index_filterable=False,
                    index_range_filters=False,
                    index_searchable=False,
                ),
            ],
            vector_index_config=Configure.VectorIndex.hnsw(distance_metric=VectorDistances.COSINE),
            inverted_index_config=Configure.inverted_index(
                bm25_b=0.7,
                bm25_k1=1.25,
                index_null_state=True,
                index_property_length=True,
                index_timestamps=True,
            ),
            vectorizer_config=wvc.config.Configure.Vectorizer.text2vec_ollama(
                api_endpoint="http://ollama:11434",
                model="nomic-embed-text",
            ),
            generative_config=wvc.config.Configure.Generative.ollama(
                api_endpoint="http://ollama:11434",
                model="llama3.1",
            ),
        )
        with created_collection.batch.dynamic() as batch:
            for idx, data_obj in enumerate(data):
                print(f"{idx} ingested")
                try: 
                    batch.add_object(
                        properties=data_obj,
                        uuid=generate_uuid5(data_obj)
                    )
                except Exception as e:
                    print(f"{e} -> with {data_obj["title"]}")

        return created_collection

    except Exception as e:
        print(e)
        print(f"collection: {collection_name} already CREATED!")
        return client.collections.get(collection_name)

if __name__ == "__main__":
    translator = Translator()
    if translate:
        with open(path+".json", "r") as f:
            texts_json = json.load(f)
            texts_json_translated = translator.transform_to_eng(texts_json)
            
        with open(path+"_translated"+".json", 'w') as f:
            json.dump(texts_json_translated, f, ensure_ascii=False) 
    else:
        with open(path+".json", "r") as f:
            texts_json_translated = json.load(f)

    print(f"{len(texts_json_translated)} samples ready to ingest")

    weaviate_client = weaviate.connect_to_local()
    created_collection = ingest_to_weaviate(weaviate_client, texts_json_translated)
    print(f"{created_collection.aggregate.over_all(total_count=True)} samples created, closing client...")
    weaviate_client.close()
