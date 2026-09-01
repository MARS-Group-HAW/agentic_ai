from typing import Any

import psycopg

from src.app.settings import get_settings


def database_health() -> dict[str, Any]:
    """Return a small database/pgvector health report.

    A connection is opened only when this function is called, so the FastAPI
    service can start even when PostgreSQL is temporarily unavailable.
    """
    settings = get_settings()
    with psycopg.connect(settings.database_url, connect_timeout=3) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT version()")
            postgres_version = cur.fetchone()[0]
            cur.execute(
                "SELECT extversion FROM pg_extension WHERE extname = 'vector'"
            )
            row = cur.fetchone()

    return {
        "database": "ok",
        "postgres": postgres_version,
        "pgvector": row[0] if row else None,
    }
