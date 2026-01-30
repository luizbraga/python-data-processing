import logging
from datetime import datetime
from typing import Annotated, Any

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from fastapi_pagination import Page
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.core.db import postgres_db
from app.schemas.notes import NoteRead
from app.services.notes import NoteService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/patients/{patient_id}/notes", tags=["notes"])


def get_note_service(
    db: AsyncSession = Depends(postgres_db.get_conn),
) -> NoteService:
    """Dependency to get note service."""
    return NoteService(db)


async def validate_upload_file(file: UploadFile = File(...)) -> str:
    """Validate that uploaded file is a text file."""
    allowed_types = ["text/plain"]

    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed types: {', '.join(allowed_types)}",
        )

    # Validate file size
    content = await file.read()
    if len(content) > settings.max_upload_size:  # 10MB limit
        raise HTTPException(status_code=413, detail="File too large.")

    # Text validations
    try:
        content_str = content.decode("utf-8")
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="File must be valid UTF-8 text")

    # Validate content is not empty
    if not content_str.strip():
        raise HTTPException(status_code=400, detail="File content cannot be empty")

    return content_str.strip()


@router.post("/upload", status_code=201, response_model=NoteRead)
async def create_note_file(
    patient_id: int,
    content: Annotated[str, Depends(validate_upload_file)],
    timestamp: datetime = Form(...),
    service: NoteService = Depends(get_note_service),
) -> NoteRead:
    """Create a note from file upload."""
    try:
        note = await service.create_note(
            patient_id=patient_id, content=content, timestamp=timestamp
        )
        return note
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=Page[NoteRead])
async def list_patient_notes(
    patient_id: int,
    sort_by: str | None = None,
    service: NoteService = Depends(get_note_service),
) -> Page[NoteRead] | Any:
    """Get all notes for a specific patient."""
    return await service.get_patient_notes(patient_id, sort_by)


@router.get("/{note_id}", response_model=NoteRead)
async def get_note(
    patient_id: int,
    note_id: int,
    service: NoteService = Depends(get_note_service),
) -> NoteRead:
    """Get a specific note."""
    note = await service.get_note(note_id)
    if not note or note.get("patient_id") != patient_id:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@router.delete("/{note_id}", status_code=204)
async def delete_note(
    patient_id: int,
    note_id: int,
    service: NoteService = Depends(get_note_service),
) -> None:
    """Delete a specific note."""
    note = await service.get_note(note_id)
    if not note or note.get("patient_id") != patient_id:
        raise HTTPException(status_code=404, detail="Note not found")

    logger.info(f"Deleting note: {note} for patient_id: {patient_id}")
    await service.delete_note(note_id)
