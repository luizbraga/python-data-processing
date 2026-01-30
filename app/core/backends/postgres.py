from collections.abc import AsyncGenerator
from typing import Optional

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


class PostgresBackend:
    def __init__(self) -> None:
        self.engine: Optional[AsyncEngine] = None
        self.AsyncSessionLocal: Optional[async_sessionmaker[AsyncSession]] = None

    async def init(self, database_url: str) -> None:
        self.engine = create_async_engine(
            database_url.replace("postgresql://", "postgresql+asyncpg://"),
            echo=False,
            pool_size=10,
            max_overflow=20,
            pool_pre_ping=True,
            pool_recycle=3600,  # Recycle connections every hour
        )
        self.AsyncSessionLocal = async_sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )

    async def close(self) -> None:
        if self.engine:
            await self.engine.dispose()

    async def get_conn(self) -> AsyncGenerator[AsyncSession, None]:
        if self.AsyncSessionLocal is None:
            raise RuntimeError("Database pool is not initialized.")
        async with self.AsyncSessionLocal() as session:
            yield session
