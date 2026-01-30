from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi_pagination import Page
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import postgres_db
from app.models.patients import Patient
from app.schemas.patients import PatientCreate, PatientRead, PatientUpdate
from app.services.patients import PatientService

router = APIRouter(prefix="/patients", tags=["patients"])


async def get_patient_service(
    db: AsyncSession = Depends(postgres_db.get_conn),
) -> PatientService:
    return PatientService(db)


@router.get("/", response_model=Page[PatientRead])
async def read_patients(
    service: PatientService = Depends(get_patient_service),
    sort: Optional[str] = Query(
        None, description="Sort by field", examples=["name", "-name"]
    ),
    name: Optional[str] = Query(None, description="Filter by patient name"),
) -> Page[Patient] | Any:
    patients = await service.list_patients(sort_by=sort, name_filter=name)
    return patients


@router.get("/{patient_id}", response_model=PatientRead)
async def get_patient(
    patient_id: int, service: PatientService = Depends(get_patient_service)
) -> Patient:
    patient = await service.get_patient(patient_id)
    if patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient


@router.post("/", status_code=201, response_model=PatientRead)
async def create_patient(
    patient: PatientCreate, service: PatientService = Depends(get_patient_service)
) -> Patient:
    db_patient = await service.create_patient(patient.model_dump())
    return db_patient


@router.put("/{patient_id}", response_model=PatientRead)
async def update_patient(
    patient_id: int,
    patient: PatientUpdate,
    service: PatientService = Depends(get_patient_service),
) -> Patient:
    db_patient = await service.update_patient(
        patient_id, patient.model_dump(exclude_unset=True)
    )
    if db_patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return db_patient


@router.delete("/{patient_id}", status_code=204, response_model=None)
async def delete_patient(
    patient_id: int, service: PatientService = Depends(get_patient_service)
) -> None:
    success = await service.delete_patient(patient_id)
    if not success:
        raise HTTPException(status_code=404, detail="Patient not found")
    return None
