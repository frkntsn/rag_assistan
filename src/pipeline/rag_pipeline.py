from src.generation.local_llm import get_embedding, answer_with_context
from src.data.entities import PEOPLE, PLACES
from src.retrieval.router import route_query
from src.retrieval.retriever import retrieve, retrieve_title_chunks
from src.storage.sqlite_store import log_query

TITLE_TO_TYPE = {title: "person" for title in PEOPLE} | {title: "place" for title in PLACES}


def detect_target_titles(query: str) -> list[str]:
    q = query.lower()
    all_titles = PEOPLE + PLACES
    # Prefer longest match to avoid partial collisions.
    matches = [title for title in all_titles if title.lower() in q]
    matches.sort(key=len, reverse=True)
    return matches[:2]


def normalize_answer(answer: str) -> str:
    normalized = answer.strip()
    lower = normalized.lower()
    if lower.startswith("i don't know") or lower.startswith("i do not know"):
        return "I don't know."
    return normalized


def run_rag(query: str, top_k: int = 5):
    route = route_query(query)
    is_comparison = route == "both" and any(
        token in f" {query.lower()} " for token in ("compare", "difference", "versus", " vs ")
    )
    target_titles = detect_target_titles(query)
    effective_top_k = max(top_k, 8) if route == "both" else top_k

    if target_titles:
        per_title_k = max(2, effective_top_k // len(target_titles))
        docs: list[str] = []
        for title in target_titles:
            title_route = TITLE_TO_TYPE.get(title, "both")
            title_docs = retrieve_title_chunks(
                title=title,
                route=title_route,
                limit=per_title_k,
            )
            docs.extend(title_docs)
        # Preserve order while removing duplicates.
        docs = list(dict.fromkeys(docs))[:effective_top_k]
    else:
        query_embedding = get_embedding(query)
        result = retrieve(
            query_embedding=query_embedding,
            route=route,
            top_k=effective_top_k,
            target_titles=target_titles,
        )
        docs = result.get("documents", [[]])[0]

    if not docs:
        answer = "I don't know."
        log_query(query=query, route=route, top_k=effective_top_k, retrieved_chunks=0, answer=answer)
        return {"route": route, "answer": answer, "context_docs": []}

    context = "\n\n---\n\n".join(docs)
    answer = normalize_answer(answer_with_context(query=query, context=context, is_comparison=is_comparison))
    log_query(query=query, route=route, top_k=effective_top_k, retrieved_chunks=len(docs), answer=answer)
    return {"route": route, "answer": answer, "context_docs": docs}
