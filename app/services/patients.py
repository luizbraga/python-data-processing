import logging
from typing import Any

from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.patients import Patient

logger = logging.getLogger(__name__)


class PatientService:

    def __init__(self, db_session: AsyncSession) -> None:
        self._db = db_session

    async def list_patients(
        self, sort_by: str | None = None, name_filter: str | None = None
    ) -> Any:
        logger.debug("Listing patients from database")
        sort_field: Any = Patient.id

        # Check if sorting is ascending or descending
        is_ascending = True if sort_by and not sort_by.startswith("-") else False
        if not is_ascending and sort_by:
            sort_by = sort_by[1:]

        if getattr(Patient, sort_by or "", None) is not None:
            sort_field = getattr(Patient, sort_by)  # type: ignore
            sort_field = sort_field if is_ascending else sort_field.desc()
        if name_filter:
            logger.debug(
                f"Applying name filter: {name_filter} and sorting by {sort_by}"
            )
            return await paginate(
                self._db,
                select(Patient)
                .where(func.similarity(Patient.name, name_filter) > 0.1)
                .order_by(sort_field),
            )
        return await paginate(self._db, select(Patient).order_by(sort_field))

    async def get_patient(self, patient_id: int) -> Patient | None:
        logger.debug(f"Fetching patient with ID {patient_id}")
        result = await self._db.execute(
            select(Patient).filter(Patient.id == patient_id)
        )
        return result.scalar_one_or_none()

    async def create_patient(self, patient_data: dict) -> Patient:
        logger.debug(f"Creating new patient with data {patient_data}")
        patient = Patient(**patient_data)
        self._db.add(patient)
        await self._db.commit()
        await self._db.refresh(patient)
        return patient

    async def update_patient(
        self, patient_id: int, patient_data: dict
    ) -> Patient | None:
        logger.info(f"Updating patient with ID {patient_id} with data {patient_data}")
        patient = await self.get_patient(patient_id)
        if not patient:
            return None
        for key, value in patient_data.items():
            setattr(patient, key, value)
        await self._db.commit()
        await self._db.refresh(patient)
        return patient

    async def delete_patient(self, patient_id: int) -> bool:
        logger.info(f"Deleting patient with ID {patient_id}")
        patient = await self.get_patient(patient_id)
        if not patient:
            return False
        await self._db.delete(patient)
        await self._db.commit()
        return True
