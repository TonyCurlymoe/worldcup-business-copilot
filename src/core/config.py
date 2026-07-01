from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "World Cup Business Intelligence Copilot"
    environment: str = "development"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    frontend_api_base_url: str = "http://localhost:8000"
    openai_api_key: str | None = None
    openai_model: str = "gpt-4.1-mini"
    football_data_api_key: str | None = None
    football_data_base_url: str = "https://api.football-data.org/v4"
    news_api_key: str | None = None
    news_api_base_url: str = "https://newsapi.org/v2"
    request_timeout_seconds: float = Field(default=15.0, gt=0)


@lru_cache
def get_settings() -> Settings:
    return Settings()
