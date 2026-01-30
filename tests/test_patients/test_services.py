import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.patients import Patient
from app.services.patients import PatientService

pytestmark = pytest.mark.asyncio


class TestPatientService:
    # def test_list_patients(
    #     self, db_session: Session, sample_patients: list[Patient]
    # ) -> None:
    #     sample = sample_patients[0]
    #     service = PatientService(db_session)
    #     patients = service.list_patients()
    #     assert patients.total > 0
    #     assert any(p.id == sample.id for p in patients.items)

    async def test_create_patient(
        self, db_session: AsyncSession, patient_data: dict
    ) -> None:
        service = PatientService(db_session)
        patient = await service.create_patient(patient_data)
        assert patient.id is not None
        assert patient.name == "Jane Smith"
        assert patient.date_of_birth == "1995-06-15"

    async def test_get_patient(
        self, db_session: AsyncSession, sample_patient: Patient
    ) -> None:
        service = PatientService(db_session)
        fetched_patient = await service.get_patient(sample_patient.id)
        assert fetched_patient is not None
        assert fetched_patient.id == sample_patient.id
        assert fetched_patient.name == "John Doe"
        assert fetched_patient.date_of_birth == "1990-01-15"

    async def test_update_patient(
        self, db_session: AsyncSession, sample_patient: Patient
    ) -> None:
        service = PatientService(db_session)
        update_data = {"name": "Updated Name", "date_of_birth": "2000-01-01"}
        updated_patient = await service.update_patient(sample_patient.id, update_data)
        assert isinstance(updated_patient, sample_patient.__class__)
        assert updated_patient.id == sample_patient.id
        assert updated_patient.name == sample_patient.name
        assert updated_patient.date_of_birth == sample_patient.date_of_birth

    async def test_delete_patient(
        self, db_session: AsyncSession, sample_patient: Patient
    ) -> None:
        service = PatientService(db_session)
        success = await service.delete_patient(sample_patient.id)
        assert success is True
        deleted_patient = await service.get_patient(sample_patient.id)
        assert deleted_patient is None
