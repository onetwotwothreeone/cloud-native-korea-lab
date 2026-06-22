"""Database session helpers for local PostgreSQL and tests.

14_GWAN_PostgreSQL_Local_Docker_Compose

The default target is a local PostgreSQL container started with Docker Compose.
Tests may pass a SQLite URL explicitly so the database structure can be checked
without requiring Docker.
"""

from __future__ import annotations

import os
from contextlib import contextmanager
from collections.abc import Iterator

from sqlalchemy import Engine, create_engine, inspect, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.engine import make_url

from app.db.gwan_memory_models import Base
from app.schemas.gwan_interface import ContractBaseModel

DEFAULT_DATABASE_URL = "postgresql+psycopg://hyean:hyean_password@localhost:55432/hyean_gwan"


class DatabaseStatus(ContractBaseModel):
    database_url_safe: str
    dialect: str
    connected: bool
    tables_created: bool
    table_names: list[str]
    error: str | None = None


class DatabaseCreateTablesResult(ContractBaseModel):
    database_url_safe: str
    created: bool
    table_names: list[str]


def get_database_url() -> str:
    """Return DATABASE_URL from environment or the local Docker Compose default."""

    return os.getenv("DATABASE_URL", DEFAULT_DATABASE_URL)


def make_safe_database_url(database_url: str) -> str:
    """Hide the password before returning connection details through an API."""

    url = make_url(database_url)
    return str(url.render_as_string(hide_password=True))


def create_database_engine(database_url: str | None = None) -> Engine:
    """Create a SQLAlchemy engine.

    For PostgreSQL this expects `psycopg[binary]` to be installed and the local
    container to be running. For tests, a SQLite URL can be passed directly.
    """

    url = database_url or get_database_url()
    return create_engine(url, future=True)


def create_session_factory(engine: Engine) -> sessionmaker[Session]:
    return sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False, future=True)


@contextmanager
def session_scope(engine: Engine) -> Iterator[Session]:
    """Provide a transactional session scope."""

    session_factory = create_session_factory(engine)
    session = session_factory()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def create_memory_tables(database_url: str | None = None) -> DatabaseCreateTablesResult:
    """Create GWAN memory tables in the configured database."""

    engine = create_database_engine(database_url)
    Base.metadata.create_all(engine)
    inspector = inspect(engine)
    table_names = sorted(inspector.get_table_names())
    return DatabaseCreateTablesResult(
        database_url_safe=make_safe_database_url(database_url or get_database_url()),
        created=True,
        table_names=table_names,
    )


def get_database_status(database_url: str | None = None) -> DatabaseStatus:
    """Check whether the configured database is reachable and has GWAN tables."""

    url = database_url or get_database_url()
    safe_url = make_safe_database_url(url)
    dialect = make_url(url).get_backend_name()
    try:
        engine = create_database_engine(url)
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        inspector = inspect(engine)
        table_names = sorted(inspector.get_table_names())
        expected_tables = set(Base.metadata.tables.keys())
        tables_created = expected_tables.issubset(set(table_names))
        return DatabaseStatus(
            database_url_safe=safe_url,
            dialect=dialect,
            connected=True,
            tables_created=tables_created,
            table_names=table_names,
        )
    except SQLAlchemyError as exc:
        return DatabaseStatus(
            database_url_safe=safe_url,
            dialect=dialect,
            connected=False,
            tables_created=False,
            table_names=[],
            error=str(exc),
        )
