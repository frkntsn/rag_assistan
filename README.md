# Local Wikipedia RAG Assistant

This project is a fully local Retrieval-Augmented Generation (RAG) assistant built for BLG483E HW3.

## Stack
- Python
- Ollama (`llama3.2:3b`, `nomic-embed-text`)
- Chroma (single collection + metadata filtering, Option B)
- SQLite
- Streamlit UI + optional CLI

## Project Structure
- `app.py`: Streamlit chat interface
- `scripts/build_index.py`: ingestion + chunking + embedding + indexing
- `scripts/run_cli.py`: optional CLI chat
- `src/config.py`: configuration values
- `src/data/entities.py`: seed people/place lists
- `src/ingest/wikipedia_ingest.py`: Wikipedia extraction
- `src/processing/chunker.py`: chunking logic
- `src/vectorstore/chroma_store.py`: Chroma client/collection helpers
- `src/retrieval/router.py`: person/place/both routing
- `src/retrieval/retriever.py`: filtered retrieval from Chroma
- `src/generation/local_llm.py`: local embedding + answer generation
- `src/pipeline/rag_pipeline.py`: end-to-end query pipeline
- `src/storage/sqlite_store.py`: SQLite logging for ingestion/query runs
- `Product_prd.md`: product requirements document
- `recommendation.md`: production recommendations

## Setup
1. Install Python dependencies:
   - `pip install -r requirements.txt`
2. Install and run Ollama, then pull models:
   - `ollama pull llama3.2:3b`
   - `ollama pull nomic-embed-text`
3. Optional: copy env file only if you want custom settings:
   - `cp .env.example .env`

## Run
1. Build index:
   - `python scripts/build_index.py`
2. Start UI:
   - `streamlit run app.py`
3. Optional CLI:
   - `python scripts/run_cli.py`

## Example Queries
- `Who was Albert Einstein and what is he known for?`
- `Where is the Eiffel Tower located?`
- `Which famous place is located in Turkey?`
- `Compare Albert Einstein and Nikola Tesla.`
- `Compare the Eiffel Tower and the Statue of Liberty.`
- `Who is the president of Mars?`

## Demo Video
- 

## Notes
- Seed list now contains 20 people + 20 places (including the mandatory assignment entities).
- Option B is implemented with one Chroma collection and `type` metadata filtering.
- SQLite is used to log ingestion runs and query history.
- UI includes both `Clear chat` and `Reset system` actions.
