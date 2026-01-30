import pytest
from fastapi_pagination import Params, set_params
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.patients import Patient
from app.services.patients import PatientService

pytestmark = pytest.mark.asyncio


async def test_list_patients_empty(db_session: AsyncSession) -> None:
    set_params(Params(size=10, page=1))
    service = PatientService(db_session)
    patients = await service.list_patients()
    assert patients.total == 0


async def test_list_patients(
    db_session: AsyncSession, sample_patients: list[Patient]
) -> None:
    set_params(Params(size=10, page=2))
    service = PatientService(db_session)
    patients = await service.list_patients()
    assert patients.total == len(sample_patients)

    patients = await service.list_patients(name_filter="Alice")
    assert patients.total == 1

    patients = await service.list_patients(sort_by="-date_of_birth")
    assert patients.total == len(sample_patients)
    dates = [patient.date_of_birth for patient in patients.items]
    assert dates == sorted(dates, reverse=True)


async def test_create_patient(db_session: AsyncSession, patient_data: dict) -> None:
    service = PatientService(db_session)
    patient = await service.create_patient(patient_data)
    assert patient.id is not None
    assert patient.name == "Jane Smith"
    assert patient.date_of_birth == "1995-06-15"


async def test_get_patient(db_session: AsyncSession, sample_patient: Patient) -> None:
    service = PatientService(db_session)
    fetched_patient = await service.get_patient(sample_patient.id)
    assert fetched_patient is not None
    assert fetched_patient.id == sample_patient.id
    assert fetched_patient.name == "John Doe"
    assert fetched_patient.date_of_birth == "1990-01-15"


async def test_update_patient(
    db_session: AsyncSession, sample_patient: Patient
) -> None:
    service = PatientService(db_session)
    update_data = {"name": "Updated Name", "date_of_birth": "2000-01-01"}
    updated_patient = await service.update_patient(sample_patient.id, update_data)
    assert isinstance(updated_patient, sample_patient.__class__)
    assert updated_patient.id == sample_patient.id
    assert updated_patient.name == sample_patient.name
    assert updated_patient.date_of_birth == sample_patient.date_of_birth


async def test_delete_patient(
    db_session: AsyncSession, sample_patient: Patient
) -> None:
    service = PatientService(db_session)
    success = await service.delete_patient(sample_patient.id)
    assert success is True
    deleted_patient = await service.get_patient(sample_patient.id)
    assert deleted_patient is None
