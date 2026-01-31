from datetime import datetime

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.notes import PatientNote
from app.models.patients import Patient


@pytest_asyncio.fixture
async def sample_patient(db_session: AsyncSession) -> Patient:
    """Create a sample patient for testing."""
    patient = Patient(
        name="John Doe",
        date_of_birth="1990-01-15",
    )
    db_session.add(patient)
    await db_session.commit()
    await db_session.refresh(patient)
    return patient


@pytest_asyncio.fixture
async def sample_patient_notes(
    db_session: AsyncSession, sample_patient: Patient
) -> list[PatientNote]:
    """Create sample notes for a patient."""
    notes = [
        PatientNote(
            patient_id=sample_patient.id,
            timestamp=datetime(2023, 1, 1, 10, 0, 0),
            content="Patient is recovering well.",
        ),
        PatientNote(
            patient_id=sample_patient.id,
            timestamp=datetime(2023, 1, 15, 14, 30, 0),
            content="Follow-up visit shows improvement.",
        ),
    ]
    db_session.add_all(notes)
    await db_session.commit()
    for note in notes:
        await db_session.refresh(note)
    return notes
