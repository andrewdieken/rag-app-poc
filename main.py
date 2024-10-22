import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from data_loader import load_data
from utils import get_embedding_model, get_es_client

load_dotenv()

# Set the TOKENIZERS_PARALLELISM environment variable
os.environ["TOKENIZERS_PARALLELISM"] = "false"

es_client = get_es_client()

openai_client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)

index_source_fields = {
    "rag_poc": [
        "context"
    ]
}

embedding_model = get_embedding_model()


def get_query_embedding(query):
    return embedding_model.encode(query).tolist()


def get_elasticsearch_results(query_text):
    knn_query = {
        "field": "context_embedding",
        "k": 8,
        "num_candidates": 100,
        "query_vector": get_query_embedding(query_text),
        "boost": 100,
    }
    result = es_client.search(index='rag_poc', body={"knn": knn_query, "_source": ["context"]})
    return result["hits"]["hits"]


def create_openai_prompt(results):
    context = ""
    for hit in results:
        source_field = index_source_fields.get(hit["_index"])[0]
        hit_context = hit["_source"][source_field]
        context += f"{hit_context}\n"
    prompt = f"""
Instructions:

- You are an assistant for question-answering tasks.
- Answer questions truthfully and factually using only the context presented.
- If you don't know the answer, just say that you don't know, don't make up an answer.
- You must always cite the document where the answer was extracted using inline academic citation style [], using the position.
- Use markdown format for code examples.
- You are correct, factual, precise, and reliable.

Context:
{context}

"""
    return prompt


def generate_openai_completion(user_prompt, question):
    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": user_prompt},
            {"role": "user", "content": question},
        ]
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    while True:
        print("Please select an option:")
        print("1. Ask a question")
        print("2. Load data")
        print("3. Exit")

        option = input("Please enter your choice: ")

        if option == "1":
            question = input("Please enter your question: ")
            elasticsearch_results = get_elasticsearch_results(question)
            context_prompt = create_openai_prompt(elasticsearch_results)
            openai_completion = generate_openai_completion(context_prompt, question)
            print(openai_completion)
        elif option == "2":
            file_path = input("Please enter the path to the JSON file: ")
            load_data(file_path)
        elif option == "3":
            break
        else:
            print("Invalid option")
