from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.models.patients import Patient
from app.schemas.patients import PatientCreate, PatientRead, PatientUpdate

router = APIRouter(prefix="/patients", tags=["patients"])


@router.get("/", response_model=list[PatientRead])
def read_patients(db: Session = Depends(get_db)) -> list[Patient]:
    patients = db.query(Patient).all()
    return patients


@router.get("/{patient_id}", response_model=PatientRead)
def get_patient(patient_id: int, db: Session = Depends(get_db)) -> Patient:
    db_patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if db_patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return db_patient


@router.post("/", status_code=201, response_model=PatientRead)
def create_patient(patient: PatientCreate, db: Session = Depends(get_db)) -> Patient:
    db_patient = Patient(**patient.model_dump())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient


@router.put("/{patient_id}", response_model=PatientRead)
def update_patient(
    patient_id: int, patient: PatientUpdate, db: Session = Depends(get_db)
) -> Patient:
    db_patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if db_patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    for key, value in patient.model_dump(exclude_unset=True).items():
        setattr(db_patient, key, value)
    db.commit()
    db.refresh(db_patient)
    return db_patient


@router.delete("/{patient_id}", status_code=204, response_model=None)
def delete_patient(patient_id: int, db: Session = Depends(get_db)) -> None:
    db_patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if db_patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    db.delete(db_patient)
    db.commit()
    return None
