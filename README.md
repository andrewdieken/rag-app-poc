# RAG Application Proof of Concept

This project demonstrates a Retrieval-Augmented Generation (RAG) application leveraging the following technologies:

1. Elasticsearch: Utilized as a vector database for efficient storage and retrieval of context embeddings.
2. Sentence Transformers: Used for creating dense vector embeddings of query and context data (the [avsolatorio/GIST-all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) model is used).
3. OpenAI: Employed for generating human-like responses based on retrieved context (the `gpt-3.5-turbo` model is used).

The purpose of this proof of concept is to illustrate how RAG can enhance question-answering applications by combining the strengths of pre-trained language models with the ability to retrieve relevant information from a large corpus of private data. This approach allows for more accurate, context-aware responses while maintaining the flexibility to incorporate up-to-date information.

Key features of this RAG application include:
- Dynamic relevant context retrieval based on user queries using Elasticsearch's kNN search
- Integration with OpenAI's language models for natural language generation
- A simple command-line interface for interacting with the system

This project serves as a starting point in exploring RAG architectures and their potential applications.

## Setup

1. Install dependencies: `pip install -r requirements.txt`
4. Set up environment variables: `cp .env.sample .env`
    - `ELASTIC_PASSWORD` should be the password for your Elasticsearch instance.
    - `KIBANA_PASSWORD` should be the password for your Kibana instance.
2. Start up Elasticsearch and Kibana: `docker compose up -d`
3. Create an API key for your Elasticsearch instance.
    - Go to Kibana (http://localhost:5601) and navigate to Management > Stack Management > API Keys.
    - Click "Create API Key".
    - Enter a name for the API key.
    - Click "Create API Key".
    - Copy the API key ID and API key.
4. In the `.env` file, set the `ES_API_KEY` to the API key for your Elasticsearch instance you created in the previous step.
5. In the `.env` file, set the `OPENAI_API_KEY` to your OpenAI API key.

## Usage

### Loading Data

Run the script: `python main.py` and when prompted, select option 2 and provide the path to the JSON file you'd like to load into Elasticsearch.

Note, you can load multiple files into Elasticsearch by continually selecting option 2.

An example JSON file is provided in the `example_data.json` file.

### Asking Questions

Run the script: `python main.py` and when prompted, select option 1 and ask a question about the loaded data.

## Notes

- Kibana can be accessed at http://localhost:5601 with the `elastic` user using the `KIBANA_PASSWORD` you set in the `.env` file.
- The embedding model used is [avsolatorio/GIST-all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2).
