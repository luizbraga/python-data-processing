from collections.abc import AsyncGenerator, Generator
from unittest.mock import AsyncMock

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_utils import create_database, database_exists, drop_database

import alembic
from alembic.config import Config
from app.config import settings
from app.core.db import postgres_db
from app.main import app
from app.routes.patients import get_patient_service

TEST_DATABASE_URL = f"{settings.database_url}_test"
settings.database_url = TEST_DATABASE_URL

if database_exists(TEST_DATABASE_URL):
    drop_database(TEST_DATABASE_URL)

create_database(TEST_DATABASE_URL)


@pytest.fixture(scope="session")
def setup_test_database() -> Generator[None, None, None]:
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", TEST_DATABASE_URL)
    alembic.command.upgrade(alembic_cfg, "head")

    yield

    alembic.command.downgrade(alembic_cfg, "base")


@pytest_asyncio.fixture(scope="function", autouse=True)
async def init_db(setup_test_database: None) -> AsyncGenerator[None, None]:
    """Initialize database connection for each test."""
    await postgres_db.init(TEST_DATABASE_URL)
    yield
    await postgres_db.close()


@pytest_asyncio.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Provide a database session for tests with rollback."""
    if postgres_db.AsyncSessionLocal is None:
        raise RuntimeError("Database pool is not initialized.")
    async with postgres_db.AsyncSessionLocal() as session:
        yield session
        await session.rollback()


@pytest_asyncio.fixture(scope="function")
async def client() -> AsyncGenerator[AsyncClient, None]:
    """Provide an async HTTP client."""
    async with AsyncClient(app=app, base_url="http://test") as app_client:
        yield app_client


@pytest_asyncio.fixture
async def client_with_mock_service(
    mock_patient_service: AsyncMock,
) -> AsyncGenerator[AsyncClient, None]:
    """Create a test client with mocked service"""
    app.dependency_overrides[get_patient_service] = lambda: mock_patient_service
    async with AsyncClient(app=app, base_url="http://test") as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
def mock_patient_service() -> AsyncMock:
    """Create a mock PatientService"""
    return AsyncMock()
