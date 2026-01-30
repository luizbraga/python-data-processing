from sqlalchemy.orm import declarative_base

from app.core.backends.postgres import PostgresBackend

Base = declarative_base()
postgres_db = PostgresBackend()
