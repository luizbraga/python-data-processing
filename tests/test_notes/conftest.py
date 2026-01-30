import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

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
