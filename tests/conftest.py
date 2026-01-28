"""Test configuration and fixtures.

This module provides test fixtures for the FastAPI application with Alembic models.

Database Setup:
    - Uses in-memory SQLite for fast, isolated tests
    - Tables are created/dropped for each test function
    - All models are registered with SQLAlchemy's Base

Core Fixtures:
    - setup_database: Auto-creates/drops tables for each test
    - db_session: Provides database session for each test
    - client: TestClient with overridden database dependency
    - sample_patient: Example patient record for testing

Creating New Model Fixtures:
    To create fixtures for other models, follow this pattern:

    @pytest.fixture
    def sample_<model_name>(db_session: Session) -> <ModelClass>:
        '''Create a sample <model> for testing.'''
        instance = <ModelClass>(
            field1="value1",
            field2="value2",
            # ... all required fields
        )
        db_session.add(instance)
        db_session.commit()
        db_session.refresh(instance)  # Populate auto-generated fields
        return instance

    For multiple instances:

    @pytest.fixture
    def sample_<model_plural>(db_session: Session) -> list[<ModelClass>]:
        '''Create multiple <model> records for testing.'''
        instances = [
            <ModelClass>(field1="value1", ...),
            <ModelClass>(field1="value2", ...),
        ]
        db_session.add_all(instances)
        db_session.commit()
        for instance in instances:
            db_session.refresh(instance)
        return instances

Usage in Tests:
    def test_something(client: TestClient, sample_patient: Patient):
        # The fixture is automatically resolved and injected
        response = client.get(f"/patients/{sample_patient.id}")
        assert response.status_code == 200
"""

from typing import Generator
from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.db import Base, get_db
from app.main import app
from app.models.patients import Patient  # noqa: F401 - Import models to register them
from app.routes.patients import get_patient_service

# Shared in-memory SQLite for tests
engine = create_engine(
    "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


@pytest.fixture(scope="function", autouse=True)
def setup_database() -> Generator[None, None, None]:
    """Create tables before each test and drop after."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session() -> Generator[Session, None, None]:
    """Provide a database session for tests."""
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(scope="function")
def client(db_session: Session) -> Generator[TestClient, None, None]:
    """Create a test client with database dependency override."""

    def _get_test_db() -> Generator[Session, None, None]:
        """Override database dependency to use test session."""
        yield db_session

    app.dependency_overrides[get_db] = _get_test_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture
def mock_patient_service() -> Mock:
    """Create a mock PatientService"""
    return Mock()


@pytest.fixture
def client_with_mock_service(
    mock_patient_service: Mock,
) -> Generator[TestClient, None, None]:
    """Create a test client with mocked service"""
    app.dependency_overrides[get_patient_service] = lambda: mock_patient_service
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def sample_patient(db_session: Session) -> Patient:
    """Create a sample patient for testing."""
    patient = Patient(
        first_name="John",
        last_name="Doe",
        date_of_birth="1990-01-15",
        medical_record_number="MRN001234",
    )
    db_session.add(patient)
    db_session.commit()
    db_session.refresh(patient)
    return patient


@pytest.fixture
def sample_patients(db_session: Session) -> list[Patient]:
    """Create multiple patients for testing list operations."""
    patients = [
        Patient(
            first_name="Alice",
            last_name="Smith",
            date_of_birth="1985-03-20",
            medical_record_number="MRN001001",
        ),
        Patient(
            first_name="Bob",
            last_name="Johnson",
            date_of_birth="1992-07-10",
            medical_record_number="MRN001002",
        ),
        Patient(
            first_name="Carol",
            last_name="Williams",
            date_of_birth="1988-11-05",
            medical_record_number="MRN001003",
        ),
    ]
    db_session.add_all(patients)
    db_session.commit()
    for patient in patients:
        db_session.refresh(patient)
    return patients


@pytest.fixture
def patient_data() -> dict:
    """Provide valid patient data dict for create/update operations."""
    return {
        "first_name": "Jane",
        "last_name": "Smith",
        "date_of_birth": "1995-06-15",
        "medical_record_number": "MRN999999",
    }
