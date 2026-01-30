"""Models package - imports all SQLAlchemy models for Alembic discovery."""

from app.models.notes import PatientNote
from app.models.patients import Patient

__all__ = ["Patient", "PatientNote"]
