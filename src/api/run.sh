#!/bin/bash

sudo docker start ollama-weaviate weaviate-local
sleep 5
fastapi run server.py