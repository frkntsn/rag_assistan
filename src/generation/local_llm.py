import ollama

from src.config import settings

client = ollama.Client(host=settings.ollama_base_url)


def get_embedding(text: str) -> list[float]:
    response = client.embeddings(model=settings.embed_model, prompt=text)
    return response["embedding"]


def answer_with_context(query: str, context: str, is_comparison: bool = False) -> str:
    if is_comparison:
        instructions = (
            "You are a grounded assistant.\n"
            "Use only the provided context.\n"
            "If the context clearly lacks the needed facts, respond with exactly: I don't know.\n"
            "This is a comparison question. Mention each entity separately with 1-2 key facts from context.\n"
            "Keep the comparison concise.\n"
            "Do not infer roles/professions unless explicitly supported by context text.\n"
            "Do not use outside knowledge.\n\n"
        )
    else:
        instructions = (
            "You are a grounded assistant.\n"
            "Use only the provided context.\n"
            "If the context clearly lacks the needed facts, respond with exactly: I don't know.\n"
            "Answer directly in 1-3 sentences.\n"
            "Do not add unrelated entities or extra sections.\n"
            "Do not use outside knowledge.\n\n"
        )

    prompt = (
        f"{instructions}"
        f"Question: {query}\n\n"
        f"Context:\n{context}\n\n"
        "Answer:"
    )
    response = client.chat(
        model=settings.llm_model,
        messages=[{"role": "user", "content": prompt}],
        options={"temperature": 0.1},
    )
    return response["message"]["content"].strip()
