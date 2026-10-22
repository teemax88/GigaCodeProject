from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ApiSettings(BaseSettings):
    """API environment configuration."""

    base_url: str = Field(
        ..., description="Base URL for API endpoints"
    )
    timeout: int = Field(
        30, description="Request timeout in seconds"
    )
    default_headers: dict = Field(
        default_factory=dict, description="Default headers for all requests"
    )
    retry_count: int = Field(
        0, description="Number of retries on failure"
    )
    retry_delay: int = Field(
        1, description="Delay between retries in seconds"
    )

    model_config = SettingsConfigDict(
        env_prefix="API_",
        env_file=(".env", ".env.local"),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


class ApiDevSettings(ApiSettings):
    """API development environment."""

    base_url: str = "http://localhost:8000"
    timeout: int = 30
    retry_count: int = 0


class ApiStagingSettings(ApiSettings):
    """API staging environment."""

    base_url: str = "https://staging-api.example.com"
    timeout: int = 30
    retry_count: int = 1


class ApiProdSettings(ApiSettings):
    """API production environment."""

    base_url: str = "https://api.example.com"
    timeout: int = 60
    retry_count: int = 2
