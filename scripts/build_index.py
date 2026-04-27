import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.data.entities import PEOPLE, PLACES
from src.ingest.wikipedia_ingest import fetch_wikipedia_extract
from src.processing.chunker import chunk_text
from src.generation.local_llm import get_embedding
from src.vectorstore.chroma_store import upsert_chunks
from src.storage.sqlite_store import init_sqlite, log_ingestion_run


def build_index():
    init_sqlite()
    items = [("person", name) for name in PEOPLE] + [("place", name) for name in PLACES]

    total_chunks = 0

    print(f"Starting indexing for {len(items)} entities...", flush=True)

    for idx, (entity_type, title) in enumerate(items, start=1):
        print(f"[{idx}/{len(items)}] Fetching {entity_type}: {title}", flush=True)
        try:
            text = fetch_wikipedia_extract(title)
        except Exception as exc:
            print(f"  - Skipped {title} (fetch error: {exc})", flush=True)
            continue

        chunks = chunk_text(text)
        if not chunks:
            print(f"  - Skipped {title} (empty extract)", flush=True)
            continue

        print(f"  - {len(chunks)} chunks", flush=True)
        entity_ids = []
        entity_docs = []
        entity_embeddings = []
        entity_metadatas = []

        for i, chunk in enumerate(chunks):
            # Keep title/type in document text so semantic retrieval is more entity-aware.
            enriched_chunk = f"Title: {title}\nType: {entity_type}\n\n{chunk}"
            try:
                embedding = get_embedding(enriched_chunk)
            except Exception as exc:
                print(f"  - Embedding failed for {title} chunk {i}: {exc}", flush=True)
                continue

            entity_ids.append(f"{entity_type}:{title}:{i}")
            entity_docs.append(enriched_chunk)
            entity_embeddings.append(embedding)
            entity_metadatas.append({"type": entity_type, "title": title, "chunk_index": i})

        if not entity_docs:
            print(f"  - Skipped {title} (no chunk embedded)", flush=True)
            continue

        upsert_chunks(
            ids=entity_ids,
            documents=entity_docs,
            embeddings=entity_embeddings,
            metadatas=entity_metadatas,
        )
        total_chunks += len(entity_docs)
        print(f"  - Indexed {len(entity_docs)} chunks for {title}", flush=True)

    if total_chunks == 0:
        print("No chunks were indexed. Check network access and entity titles.", flush=True)
        return

    log_ingestion_run(total_entities=len(items), total_chunks=total_chunks)
    print(f"Indexed {total_chunks} chunks in total.", flush=True)


if __name__ == "__main__":
    build_index()
