from __future__ import annotations

from typing import TYPE_CHECKING, List

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base

if TYPE_CHECKING:
    from app.models.notes import PatientNote


class Patient(Base):
    __tablename__ = "patients"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    date_of_birth: Mapped[str] = mapped_column(String(10), nullable=False)
    created_at: Mapped[str] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )
    updated_at: Mapped[str] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    # Relationship to notes
    notes: Mapped[List[PatientNote]] = relationship(
        "PatientNote", back_populates="patient", cascade="all, delete-orphan"
    )
