import json
import weaviate
from weaviate.collections.collection import Collection
from weaviate.classes.config import Configure, Property, DataType, Tokenization, VectorDistances
from weaviate import classes as wvc
from weaviate.util import generate_uuid5

from Translator import Translator
from custom_types import DataObj

collection_name = "bratislava_articles_example"

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
                    name="paragraph",
                    data_type=DataType.TEXT,
                    vectorize_property_name=False,
                    tokenization=Tokenization.WORD,
                    index_searchable=True,
                ),
                # disabled indexing for source urls
                Property(
                    name="sources",
                    data_type=DataType.TEXT_ARRAY,
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
            for data_obj in data:
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
    with open("src/index/data/ingest_data_example.json") as f:
        texts_json = json.load(f)

    translator = Translator(stream=False)
    texts_json_translated = translator.transform_to_eng(texts_json)
    print(f"{len(texts_json_translated)} samples ready to ingest")

    weaviate_client = weaviate.connect_to_local()
    created_collection = ingest_to_weaviate(weaviate_client, texts_json_translated)
    print(f"{created_collection.aggregate.over_all(total_count=True)} samples created, closing client...")
    weaviate_client.close()
