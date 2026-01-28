"""Models package - imports all SQLAlchemy models for Alembic discovery."""

from app.models.patients import Patient

__all__ = ["Patient"]
