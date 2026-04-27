import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.pipeline.rag_pipeline import run_rag


def main():
    print("Local Wikipedia RAG CLI. Type 'exit' to quit.")
    while True:
        query = input("\nQuestion> ").strip()
        if query.lower() in {"exit", "quit"}:
            break
        result = run_rag(query)
        print(f"\nRoute: {result['route']}")
        print(f"Answer: {result['answer']}")


if __name__ == "__main__":
    main()
