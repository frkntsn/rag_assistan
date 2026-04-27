# Production Deployment Recommendation

## Current MVP Constraints
- Designed for local execution and coursework requirements.
- Uses local Ollama runtime and local Chroma persistence.

## Recommended Production Direction
- Containerize app, Ollama, and vector store using Docker Compose.
- Keep Option B metadata filtering for flexibility in mixed queries.
- Add robust monitoring (latency, retrieval hit quality, failure cases).
- Introduce caching for repeated queries and embeddings.
- Add automated ingestion refresh jobs and data versioning.

## Risks and Mitigations
- **Model latency on low-resource devices:** use smaller models, cache outputs.
- **Hallucinations:** strict prompt grounding and low-temperature generation.
- **Data staleness:** periodic re-ingestion and incremental indexing.

## Scaling Notes
- Replace local-only setup with managed vector DB when needed.
- Add API service layer (FastAPI) before front-end scaling.
- Keep metadata schema stable to support future filtering/reranking.
