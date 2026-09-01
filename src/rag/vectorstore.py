"""Minimal pgvector integration helpers.

This is infrastructure only. Document loading, chunking, indexing strategy,
retrieval policy, metadata design and evaluation remain team work.
"""

from typing import Any

from langchain_postgres import PGEngine, PGVectorStore

from src.app.settings import Settings, get_settings
from src.llm.factory import get_embeddings


def get_pg_engine(settings: Settings | None = None) -> PGEngine:
    settings = settings or get_settings()
    return PGEngine.from_connection_string(url=settings.langchain_postgres_url)


def initialize_vector_store(
    *,
    table_name: str,
    vector_size: int,
    embeddings: Any | None = None,
    settings: Settings | None = None,
) -> PGVectorStore:
    """Create the course-standard PGVectorStore table and return the store.

    Call this explicitly from a setup/ingestion step, not during application
    import. Teams must choose an embedding model and therefore know its vector
    dimension before initializing the table.
    """
    settings = settings or get_settings()
    engine = get_pg_engine(settings)
    engine.init_vectorstore_table(table_name=table_name, vector_size=vector_size)
    return PGVectorStore.create_sync(
        engine=engine,
        table_name=table_name,
        embedding_service=embeddings or get_embeddings(settings),
    )


def open_vector_store(
    *,
    table_name: str,
    embeddings: Any | None = None,
    settings: Settings | None = None,
) -> PGVectorStore:
    """Open an already initialized PGVectorStore."""
    settings = settings or get_settings()
    return PGVectorStore.create_sync(
        engine=get_pg_engine(settings),
        table_name=table_name,
        embedding_service=embeddings or get_embeddings(settings),
    )
