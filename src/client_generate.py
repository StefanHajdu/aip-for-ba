import weaviate

collection_name = "bratislava_articles_example"
prompt = "Why is Bratislava the ritches region in Slovakia?"

weaviate_client = weaviate.connect_to_local()
collection_ba = weaviate_client.collections.get(collection_name)

response = collection_ba.generate.near_text(
    query=prompt,
    single_prompt=prompt + " Title: {title} text: {paragraph}",
    limit=1,
)

for obj in response.objects:
    print(f"Searched in: {obj.properties["title"]}")
    print(obj.generated)

weaviate_client.close()
