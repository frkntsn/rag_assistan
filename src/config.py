from pydantic import BaseModel
import os


class Settings(BaseModel):
    ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    llm_model: str = os.getenv("LLM_MODEL", "llama3.2:3b")
    embed_model: str = os.getenv("EMBED_MODEL", "nomic-embed-text")
    chroma_dir: str = os.getenv("CHROMA_DIR", "./data/chroma")
    sqlite_path: str = os.getenv("SQLITE_PATH", "./data/app.db")
    collection_name: str = os.getenv("COLLECTION_NAME", "wiki_entities")


settings = Settings()
