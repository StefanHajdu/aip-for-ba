import json
import requests as r
from pathlib import Path
import polars as pl
from ollama import Client
# cwith ontext size 12k


DATA_PATH = "/workspace/aip-for-ba/data"
client = Client(host='http://192.168.0.199:11434')


with open(f"{DATA_PATH}/ingest_data_datasets.json", "r") as f:
    datasets = json.load(f)

for dataset in datasets:
    dataset_url = dataset['table']
    response = r.get(dataset_url)
    if response.status_code != 200:
        print(f'Error downloading data from {dataset_url}')
        continue

    try:
        rows = [row.get('attributes') for row in response.json().get('features')]
        file_path = f'{DATA_PATH}/data_bratislava/{dataset["title"]}.ndjson'
        with open(file_path, 'w', encoding='utf-8') as f:
            for row in rows: 
                f.write(json.dumps(row, ensure_ascii=False) + '\n')

        if Path(file_path).stat().st_size == 0:
            print(f'{dataset["title"]} is empty')
            continue

        data = pl.read_ndjson(file_path)
        response = client.generate(model='llama3.1', options={"num_ctx": 12000}, prompt=f'Write description of this dataset, what columns it has, what values are there and the ranges: {data.describe()}')['response']
        dataset.update(response)

    except Exception:
        print(f'No features in {dataset_url}')


with open(f"{DATA_PATH}/ingest_data_datasets_with_description.json", "w") as f:
    json.dump(datasets, f, indent=4, ensure_ascii=False)