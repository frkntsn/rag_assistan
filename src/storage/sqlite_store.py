import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from src.config import settings


def _connect() -> sqlite3.Connection:
    db_path = Path(settings.sqlite_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(db_path)


def init_sqlite() -> None:
    with _connect() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS ingestion_runs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT NOT NULL,
                total_entities INTEGER NOT NULL,
                total_chunks INTEGER NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS query_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT NOT NULL,
                query TEXT NOT NULL,
                route TEXT NOT NULL,
                top_k INTEGER NOT NULL,
                retrieved_chunks INTEGER NOT NULL,
                answer TEXT NOT NULL
            )
            """
        )
        conn.commit()


def log_ingestion_run(total_entities: int, total_chunks: int) -> None:
    init_sqlite()
    now = datetime.now(timezone.utc).isoformat()
    with _connect() as conn:
        conn.execute(
            """
            INSERT INTO ingestion_runs(created_at, total_entities, total_chunks)
            VALUES (?, ?, ?)
            """,
            (now, total_entities, total_chunks),
        )
        conn.commit()


def log_query(query: str, route: str, top_k: int, retrieved_chunks: int, answer: str) -> None:
    init_sqlite()
    now = datetime.now(timezone.utc).isoformat()
    with _connect() as conn:
        conn.execute(
            """
            INSERT INTO query_logs(created_at, query, route, top_k, retrieved_chunks, answer)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (now, query, route, top_k, retrieved_chunks, answer),
        )
        conn.commit()


def clear_sqlite_logs() -> None:
    init_sqlite()
    with _connect() as conn:
        conn.execute("DELETE FROM ingestion_runs")
        conn.execute("DELETE FROM query_logs")
        conn.commit()
