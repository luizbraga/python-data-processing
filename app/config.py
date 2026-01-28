"""Application configuration using pydantic-settings."""
from typing import Any

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    app_name: str = "Python Data Processing API"
    debug: bool = False
    database_url: str = "sqlite:///./test.db"

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)


def get_settings() -> Settings:
    """Get application settings instance."""
    return Settings()


settings = get_settings()
