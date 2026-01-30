import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.patients import Patient  # noqa: F401 - Import models to register them


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
async def sample_patients(db_session: AsyncSession) -> list[Patient]:
    """Create multiple patients for testing list operations."""
    patients = [
        Patient(
            name="Alice Johnson",
            date_of_birth="1985-03-20",
        ),
        Patient(
            name="Bob Smith",
            date_of_birth="1992-07-10",
        ),
        Patient(
            name="Carol Williams",
            date_of_birth="1988-11-05",
        ),
    ]
    db_session.add_all(patients)
    await db_session.commit()
    for patient in patients:
        await db_session.refresh(patient)
    return patients


@pytest_asyncio.fixture
async def patient_data() -> dict:
    """Provide valid patient data dict for create/update operations."""
    return {
        "name": "Jane Smith",
        "date_of_birth": "1995-06-15",
    }
