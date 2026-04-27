from typing import List, Dict, Any
from pathlib import Path
import chromadb
from chromadb.config import Settings

from src.config import settings


def get_client() -> chromadb.ClientAPI:
    Path(settings.chroma_dir).mkdir(parents=True, exist_ok=True)
    return chromadb.PersistentClient(
        path=settings.chroma_dir,
        settings=Settings(anonymized_telemetry=False),
    )


def get_collection():
    client = get_client()
    return client.get_or_create_collection(name=settings.collection_name)


def upsert_chunks(
    ids: List[str],
    documents: List[str],
    embeddings: List[List[float]],
    metadatas: List[Dict[str, Any]],
) -> None:
    collection = get_collection()
    collection.upsert(ids=ids, documents=documents, embeddings=embeddings, metadatas=metadatas)


def reset_collection() -> None:
    client = get_client()
    try:
        client.delete_collection(name=settings.collection_name)
    except Exception:
        # Collection may not exist yet; keep reset idempotent.
        pass
    client.get_or_create_collection(name=settings.collection_name)
