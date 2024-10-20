# Schedule Search RAG Application POC

This is a proof of concept for a RAG application that allows users to search for sessions in a schedule.

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
6. Create and populate the index: `python es_config.py --file-path /path/to/schedule.csv`

## Usage

Run the script: `python main.py` and when prompted, enter a question about the schedule.

## Notes

- Kibana can be accessed at http://localhost:5601 with the `elastic` user using the `KIBANA_PASSWORD` you set in the `.env` file.
- The embedding model used is [avsolatorio/GIST-all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2).
