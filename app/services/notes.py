import logging
from datetime import datetime
from typing import Any, Sequence

from fastapi_pagination.ext.sqlalchemy import apaginate
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.notes import PatientNote
from app.models.patients import Patient

logger = logging.getLogger(__name__)


class NoteService:
    def __init__(self, db_session: AsyncSession) -> None:
        self._db = db_session

    async def create_note(
        self, patient_id: int, content: str, timestamp: datetime
    ) -> PatientNote:
        """Create a new note for a patient."""
        logger.info(f"Creating note for patient {patient_id}")

        # Verify patient exists
        result = await self._db.execute(
            select(Patient).filter(Patient.id == patient_id)
        )
        patient = result.scalar_one_or_none()
        if not patient:
            raise ValueError(f"Patient with id {patient_id} not found")

        note = PatientNote(patient_id=patient_id, content=content, timestamp=timestamp)
        self._db.add(note)
        await self._db.commit()
        await self._db.refresh(note)
        return note

    async def get_patient_notes(
        self, patient_id: int, sort_by: str | None = None
    ) -> Any:
        """Get all notes for a specific patient with pagination."""
        logger.debug(f"Fetching notes for patient {patient_id}")

        sort_field = PatientNote.timestamp.desc()  # Default: newest first

        if sort_by:
            is_ascending = not sort_by.startswith("-")
            field_name = sort_by[1:] if not is_ascending else sort_by

            if hasattr(PatientNote, field_name):
                sort_field = getattr(PatientNote, field_name)
                sort_field = sort_field if is_ascending else sort_field.desc()

        return await apaginate(
            self._db,
            select(PatientNote)
            .filter(PatientNote.patient_id == patient_id)
            .order_by(sort_field),
        )

    async def get_latests_patient_notes(self, patient_id: int) -> Sequence[PatientNote]:
        """Get all notes for a specific patient without pagination."""
        logger.debug(f"Fetching all notes for patient {patient_id}")
        result = await self._db.execute(
            select(PatientNote)
            .filter(PatientNote.patient_id == patient_id)
            .order_by(PatientNote.timestamp.desc())
            .limit(5)
        )
        return result.scalars().all()

    async def get_note(self, note_id: int) -> PatientNote | None:
        """Get a specific note by ID."""
        logger.debug(f"Fetching note with ID {note_id}")
        result = await self._db.execute(
            select(PatientNote).filter(PatientNote.id == note_id)
        )
        return result.scalar_one_or_none()

    async def delete_note(self, note_id: int) -> bool:
        """Delete a note."""
        logger.info(f"Deleting note with ID {note_id}")
        note = await self.get_note(note_id)
        if not note:
            return False
        await self._db.delete(note)
        await self._db.commit()
        return True

    async def delete_patient_notes(self, patient_id: int) -> int:
        """Delete all notes for a patient."""
        logger.info(f"Deleting all notes for patient {patient_id}")
        result = await self._db.execute(
            delete(PatientNote).where(PatientNote.patient_id == patient_id)
        )
        await self._db.commit()
        return result.rowcount
