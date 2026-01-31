"""Application configuration using pydantic-settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    app_name: str = "Python Data Processing API"
    debug: bool = False
    database_url: str = "sqlite:///./test.db"

    # File upload settings
    max_upload_size: int = 10 * 1024 * 1024  # 10MB
    allowed_upload_types: list[str] = ["text/plain"]

    # LLM settings
    openai_api_key: str | None = None
    llm_provider: str = "openai"  # Check llm/backends for supported providers
    llm_model: str = "gpt-4o-mini"

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)


def get_settings() -> Settings:
    """Get application settings instance."""
    return Settings()


settings = get_settings()
