import logging
from datetime import datetime
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.llm.service import LLMService
from app.services.notes import NoteService
from app.services.patients import PatientService

logger = logging.getLogger(__name__)


class PatientSummaryService:

    def __init__(
        self, patients_service: PatientService, notes_service: NoteService
    ) -> None:
        self.patients_service = patients_service
        self.notes_service = notes_service

    @classmethod
    def build(cls, db_session: AsyncSession) -> "PatientSummaryService":
        patients_service = PatientService(db_session)
        notes_service = NoteService(db_session)
        service = cls(patients_service, notes_service)
        return service

    async def generate_summary(
        self, patient_id: int, llm_service: LLMService
    ) -> dict[str, Any]:
        """Generate a comprehensive patient summary."""
        # Get patient and notes
        patient = await self.patients_service.get_patient(patient_id)
        if not patient:
            raise ValueError(f"Patient with id {patient_id} not found")

        patient_notes = await self.notes_service.get_latests_patient_notes(patient_id)

        notes_data = [
            {"timestamp": note.timestamp.isoformat(), "content": note.content}
            for note in sorted(patient_notes, key=lambda n: n.timestamp)
        ]

        # Generate AI summary
        summary_text = await llm_service.generate_patient_summary(
            patient_name=patient.name,
            date_of_birth=patient.date_of_birth,
            notes=notes_data,
        )

        return {
            "heading": {
                "patient_id": patient.id,
                "name": patient.name,
                "date_of_birth": patient.date_of_birth,
                "total_notes": len(patient_notes),
            },
            "summary": summary_text,
            "generated_at": datetime.now().isoformat(),
        }
