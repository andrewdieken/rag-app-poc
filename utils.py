import json
import os

from dotenv import load_dotenv
from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer

load_dotenv()


def get_es_client():
    return Elasticsearch(
        os.getenv("ES_HOST"),
        api_key=(json.loads(os.getenv("ES_API_KEY"))['id'], json.loads(os.getenv("ES_API_KEY"))['api_key']),
        verify_certs=False,
        ssl_show_warn=False
    )


def get_embedding_model():
    return SentenceTransformer("avsolatorio/GIST-all-MiniLM-L6-v2")
