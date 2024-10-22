import argparse
import json
import os

from dotenv import load_dotenv

from utils import get_embedding_model, get_es_client

load_dotenv()

es_client = get_es_client()

index_name = "rag_poc"

index_mappings = {
    "properties": {
        "context": {
            "type": "text"
        },
        "context_embedding": {
            "type": "dense_vector",
            "dims": 384,
            "index": True,
            "similarity": "cosine"
        }
    }
}


def index_exists():
    return es_client.indices.exists(index=index_name)


def create_index():
    if index_exists():
        print(f"Index '{index_name}' already exists. If you'd like to recreate the index, delete the existing index first with the 'delete_index' flag.")
        return

    print(f"Creating index '{index_name}'...")
    es_client.indices.create(index=index_name, mappings=index_mappings)
    print(f"Index '{index_name}' created successfully.")


def populate_index(documents):
    print(f"Populating index '{index_name}'...")
    for document in documents:
        es_client.index(index=index_name, body=document)
    print(f"Index '{index_name}' populated successfully.")


def load_data(file_path):
    if not index_exists():
        create_index()

    embedding_model = get_embedding_model()

    documents = []
    with open(file_path, "r") as f:
        data = json.load(f)
        for row in data:
            if not row.get("context"):
                raise ValueError("'context' field is required")

            vector_embedding_text = row["context"]
            documents.append({
                "context": vector_embedding_text,
                "context_embedding": embedding_model.encode(vector_embedding_text).tolist()
            })


    populate_index(documents)
