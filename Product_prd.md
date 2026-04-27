# Product PRD - Local Wikipedia RAG Assistant

## Objective
Build a fully local RAG assistant that answers questions about famous people and places using Wikipedia-derived data.

## Core Scope
- Ingest at least 20 people and 20 places from Wikipedia.
- Chunk documents for retrieval.
- Create embeddings locally via Ollama (`nomic-embed-text`).
- Store vectors in Chroma with Option B design (single collection + metadata).
- Route questions as `person`, `place`, or `both`.
- Generate answers with local LLM via Ollama.
- Return "I don't know" when answer is not grounded in retrieved context.
- Provide chat-style UI.

## User Stories
- As a user, I can ask a question about a celebrity and receive a grounded answer.
- As a user, I can ask a question about a famous place and receive a grounded answer.
- As a user, I can ask mixed/compare questions and get answers based on retrieved chunks.
- As a user, I can view retrieved context optionally.

## Non-Functional Requirements
- Runs on localhost only.
- No external LLM API.
- Reproducible setup with clear README steps.

## Out of Scope (MVP)
- Multi-user auth
- Cloud deployment
- Advanced rerank models
