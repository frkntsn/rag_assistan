from typing import Dict, Any

from src.vectorstore.chroma_store import get_collection


def retrieve_title_chunks(title: str, route: str | None = None, limit: int = 5) -> list[str]:
    collection = get_collection()
    if route in ("person", "place"):
        where_filter = {"$and": [{"title": title}, {"type": route}]}
    else:
        where_filter = {"title": title}

    result = collection.get(where=where_filter, include=["documents", "metadatas"])
    documents = result.get("documents", []) or []
    metadatas = result.get("metadatas", []) or []
    if not documents:
        return []

    paired = list(zip(documents, metadatas))
    paired.sort(key=lambda item: item[1].get("chunk_index", 10**9) if item[1] else 10**9)
    return [doc for doc, _ in paired[:limit]]


def retrieve(
    query_embedding,
    route: str,
    top_k: int = 5,
    target_titles: list[str] | None = None,
) -> Dict[str, Any]:
    collection = get_collection()
    where_filter = None
    target_titles = target_titles or []

    if route in ("person", "place") and target_titles:
        title_filter = {"title": target_titles[0]} if len(target_titles) == 1 else {
            "$or": [{"title": title} for title in target_titles]
        }
        where_filter = {"$and": [{"type": route}, title_filter]}
    elif route in ("person", "place"):
        where_filter = {"type": route}
    elif target_titles:
        where_filter = {"title": target_titles[0]} if len(target_titles) == 1 else {
            "$or": [{"title": title} for title in target_titles]
        }

    kwargs = {"query_embeddings": [query_embedding], "n_results": top_k}
    if where_filter:
        kwargs["where"] = where_filter
    return collection.query(**kwargs)
