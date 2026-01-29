from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import Page
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.models.patients import Patient
from app.schemas.patients import PatientCreate, PatientRead, PatientUpdate
from app.services.patients import PatientService

router = APIRouter(prefix="/patients", tags=["patients"])


def get_patient_service(db: Session = Depends(get_db)) -> PatientService:
    return PatientService(db)


@router.get("/", response_model=Page[PatientRead])
def read_patients(
    service: PatientService = Depends(get_patient_service),
) -> Page[Patient] | Any:
    patients = service.list_patients()
    return patients


@router.get("/{patient_id}", response_model=PatientRead)
def get_patient(
    patient_id: int, service: PatientService = Depends(get_patient_service)
) -> Patient:
    patient = service.get_patient(patient_id)
    if patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient


@router.post("/", status_code=201, response_model=PatientRead)
def create_patient(
    patient: PatientCreate, service: PatientService = Depends(get_patient_service)
) -> Patient:
    db_patient = service.create_patient(patient.model_dump())
    return db_patient


@router.put("/{patient_id}", response_model=PatientRead)
def update_patient(
    patient_id: int,
    patient: PatientUpdate,
    service: PatientService = Depends(get_patient_service),
) -> Patient:
    db_patient = service.update_patient(
        patient_id, patient.model_dump(exclude_unset=True)
    )
    if db_patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return db_patient


@router.delete("/{patient_id}", status_code=204, response_model=None)
def delete_patient(
    patient_id: int, service: PatientService = Depends(get_patient_service)
) -> None:
    success = service.delete_patient(patient_id)
    if not success:
        raise HTTPException(status_code=404, detail="Patient not found")
    return None
