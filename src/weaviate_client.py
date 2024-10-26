import weaviate

weaviate_client = weaviate.connect_to_local()
response = weaviate_client.collections.list_all(simple=False)
print(response.keys())
weaviate_client.close()
