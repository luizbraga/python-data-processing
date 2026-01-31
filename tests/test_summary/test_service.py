from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.services.summary import PatientSummaryService


class TestPatientSummaryService:

    def test_build(self) -> None:
        mock_db_session = MagicMock()
        with (
            patch(
                "app.services.summary.PatientService", return_value="patients_service"
            ) as mock_patient_service,
            patch(
                "app.services.summary.NoteService", return_value="notes_service"
            ) as mock_note_service,
        ):
            service = PatientSummaryService.build(db_session=mock_db_session)
            mock_patient_service.assert_called_once_with(mock_db_session)
            mock_note_service.assert_called_once_with(mock_db_session)
            assert service.patients_service == "patients_service"
            assert service.notes_service == "notes_service"

    @pytest.mark.asyncio
    async def test_generate_summary(self, sample_patient_notes: list) -> None:
        mock_patients_service = AsyncMock()
        mock_notes_service = AsyncMock()
        service = PatientSummaryService(
            patients_service=mock_patients_service,
            notes_service=mock_notes_service,
        )

        mock_patient = AsyncMock()
        mock_patient.id = 1
        mock_patient.name = "John Doe"
        mock_patient.date_of_birth = "1990-01-15"
        mock_patients_service.get_patient.return_value = mock_patient

        mock_notes_service.get_all_patient_notes.return_value = sample_patient_notes
        mock_llm_service = AsyncMock()
        mock_llm_service.generate_patient_summary.return_value = "Summary text"

        summary = await service.generate_summary(
            patient_id=1, llm_service=mock_llm_service
        )

        assert summary["heading"]["patient_id"] == mock_patient.id
        assert summary["heading"]["name"] == "John Doe"
        assert summary["heading"]["date_of_birth"] == "1990-01-15"
        assert summary["heading"]["total_notes"] == len(sample_patient_notes)
        assert summary["summary"] == "Summary text"
        assert "generated_at" in summary
        mock_patients_service.get_patient.assert_awaited_once_with(mock_patient.id)
        mock_notes_service.get_all_patient_notes.assert_awaited_once_with(
            mock_patient.id
        )
        mock_llm_service.generate_patient_summary.assert_awaited_once()
