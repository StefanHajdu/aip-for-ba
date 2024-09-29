import weaviate

collection_name = "bratislava_articles_example"
prompt = "Why is Bratislava the ritches region in Slovakia?"

weaviate_client = weaviate.connect_to_local()
collection_ba = weaviate_client.collections.get(collection_name)
response = collection_ba.query.hybrid(query=prompt, limit=1)

for o in response.objects:
    print(o.properties)

weaviate_client.close()
