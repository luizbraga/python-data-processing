from sqlalchemy.orm import Session

from app.models.patients import Patient


class PatientService:

    def __init__(self, db_session: Session) -> None:
        self._db = db_session

    def list_patients(self) -> list[Patient]:
        return self._db.query(Patient).all()

    def get_patient(self, patient_id: int) -> Patient | None:
        return self._db.query(Patient).filter(Patient.id == patient_id).first()

    def create_patient(self, patient_data: dict) -> Patient:
        patient = Patient(**patient_data)
        self._db.add(patient)
        self._db.commit()
        self._db.refresh(patient)
        return patient

    def update_patient(self, patient_id: int, patient_data: dict) -> Patient | None:
        patient = self.get_patient(patient_id)
        if not patient:
            return None
        for key, value in patient_data.items():
            setattr(patient, key, value)
        self._db.commit()
        self._db.refresh(patient)
        return patient

    def delete_patient(self, patient_id: int) -> bool:
        patient = self.get_patient(patient_id)
        if not patient:
            return False
        self._db.delete(patient)
        self._db.commit()
        return True
