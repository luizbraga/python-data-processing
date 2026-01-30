from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class NoteBase(BaseModel):
    """Base model for patient notes."""

    content: str = Field(min_length=1, max_length=10000, description="Note content")
    timestamp: datetime = Field(description="When the note was taken")


class NoteCreate(NoteBase):
    """Schema for creating a new note."""

    pass


class NoteUpdate(BaseModel):
    """Schema for updating a note."""

    content: Optional[str] = Field(default=None, min_length=1, max_length=10000)
    timestamp: Optional[datetime] = None


class NoteRead(NoteBase):
    """Schema for reading note data."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    patient_id: int
    created_at: datetime
