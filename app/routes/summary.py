from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import postgres_db
from app.llm.service import LLMService
from app.schemas.summary import PatientSummary
from app.services.summary import PatientSummaryService

router = APIRouter(prefix="/patients/{patient_id}", tags=["summary"])


async def get_summary_service(
    db_conn: AsyncSession = Depends(postgres_db.get_conn),
) -> PatientSummaryService:
    return PatientSummaryService.build(db_conn)


async def get_llm_service() -> LLMService:
    return LLMService()


@router.get("/summary", response_model=PatientSummary)
async def get_patient_summary(
    patient_id: int,
    summary_service: PatientSummaryService = Depends(get_summary_service),
    llm_service: LLMService = Depends(get_llm_service),
) -> dict[str, Any]:
    """Generate a comprehensive patient summary using AI."""
    try:
        summary = await summary_service.generate_summary(
            patient_id=patient_id, llm_service=llm_service
        )
        return summary
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to generate summary: {str(e)}"
        )
