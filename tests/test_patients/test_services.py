from sqlalchemy.orm import Session

from app.models.patients import Patient
from app.services.patients import PatientService


class TestPatientService:
    def test_create_patient(self, db_session: Session, patient_data: dict) -> None:
        service = PatientService(db_session)
        patient = service.create_patient(patient_data)
        assert patient.id is not None
        assert patient.first_name == "Jane"
        assert patient.last_name == "Smith"
        assert patient.date_of_birth == "1995-06-15"
        assert patient.medical_record_number == "MRN999999"

    def test_get_patient(self, db_session: Session, sample_patient: Patient) -> None:
        service = PatientService(db_session)
        fetched_patient = service.get_patient(sample_patient.id)
        assert fetched_patient is not None
        assert fetched_patient.id == sample_patient.id
        assert fetched_patient.first_name == "John"
        assert fetched_patient.last_name == "Doe"
        assert fetched_patient.date_of_birth == "1990-01-15"
        assert fetched_patient.medical_record_number == "MRN001234"

    def test_update_patient(self, db_session: Session, sample_patient: Patient) -> None:
        service = PatientService(db_session)
        update_data = {"medical_record_number": "MRN654322", "address": "101 Pine St"}
        updated_patient = service.update_patient(sample_patient.id, update_data)
        assert isinstance(updated_patient, sample_patient.__class__)
        assert updated_patient.id == sample_patient.id
        assert updated_patient.first_name == sample_patient.first_name
        assert updated_patient.last_name == sample_patient.last_name
        assert updated_patient.date_of_birth == sample_patient.date_of_birth
        assert (
            updated_patient.medical_record_number
            == update_data["medical_record_number"]
        )
        assert updated_patient.address == update_data["address"]

    def test_delete_patient(self, db_session: Session, sample_patient: Patient) -> None:
        service = PatientService(db_session)
        success = service.delete_patient(sample_patient.id)
        assert success is True
        deleted_patient = service.get_patient(sample_patient.id)
        assert deleted_patient is None
