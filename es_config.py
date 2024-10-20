import argparse
import json
import os

from dotenv import load_dotenv
from elasticsearch import Elasticsearch

from data_loader import load_data
from utils import get_es_client

load_dotenv()

es_client = get_es_client()

index_name = "rag_poc"

index_mappings = {
    "properties": {
        "name": {
            "type": "text"
        },
        "session_id": {
            "type": "integer"
        },
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


def create_index():
    if es_client.indices.exists(index=index_name):
        print(f"Index '{index_name}' already exists. If you'd like to recreate the index, delete the existing index first with the 'delete_index' flag.")
        return

    print(f"Creating index '{index_name}'...")
    es_client.indices.create(index=index_name, mappings=index_mappings)
    print(f"Index '{index_name}' created successfully.")


def populate_index(file_path):
    print(f"Populating index '{index_name}'...")
    session_data = load_data(file_path)
    for session in session_data:
        es_client.index(index=index_name, body=session)
    print(f"Index '{index_name}' populated successfully.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file-path", type=str, help="Path to the CSV file for populating the index")
    args = parser.parse_args()

    create_index()
    populate_index(args.file_path)
