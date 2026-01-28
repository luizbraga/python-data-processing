"""Test configuration and fixtures."""

import pytest
from fastapi.testclient import TestClient
from typing import Generator

from app.database import Base, engine
from app.models import Item  # noqa: F401 - Import models to register them
from app.main import app


@pytest.fixture(scope="function", autouse=True)
def setup_database() -> Generator[None, None, None]:
    """Create tables before each test and drop after."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client() -> TestClient:
    """Create a test client."""
    return TestClient(app)
