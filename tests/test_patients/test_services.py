from sqlalchemy.orm import Session

from app.models.patients import Patient
from app.services.patients import PatientService


class TestPatientService:
    def test_create_patient(self, db_session: Session, patient_data: dict) -> None:
        service = PatientService(db_session)
        patient = service.create_patient(patient_data)
        assert patient.id is not None
        assert patient.name == "Jane Smith"
        assert patient.date_of_birth == "1995-06-15"

    def test_get_patient(self, db_session: Session, sample_patient: Patient) -> None:
        service = PatientService(db_session)
        fetched_patient = service.get_patient(sample_patient.id)
        assert fetched_patient is not None
        assert fetched_patient.id == sample_patient.id
        assert fetched_patient.name == "John Doe"
        assert fetched_patient.date_of_birth == "1990-01-15"

    def test_update_patient(self, db_session: Session, sample_patient: Patient) -> None:
        service = PatientService(db_session)
        update_data = {"name": "Updated Name", "date_of_birth": "2000-01-01"}
        updated_patient = service.update_patient(sample_patient.id, update_data)
        assert isinstance(updated_patient, sample_patient.__class__)
        assert updated_patient.id == sample_patient.id
        assert updated_patient.name == sample_patient.name
        assert updated_patient.date_of_birth == sample_patient.date_of_birth

    def test_delete_patient(self, db_session: Session, sample_patient: Patient) -> None:
        service = PatientService(db_session)
        success = service.delete_patient(sample_patient.id)
        assert success is True
        deleted_patient = service.get_patient(sample_patient.id)
        assert deleted_patient is None
