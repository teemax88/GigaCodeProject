from __future__ import annotations

from pathlib import Path
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables and .env files."""

    # API Configuration
    api_base_url: str = Field(..., description="Base URL for API endpoints")
    api_timeout: int = Field(30, description="Request timeout in seconds")

    # UI Configuration
    ui_base_url: str = Field(..., description="Base URL for UI application")
    browser: Literal["chrome", "firefox", "webkit"] = Field(
        "chrome", description="Browser to use for UI tests"
    )
    browser_headless: bool = Field(
        False, description="Run browser in headless mode"
    )
    browser_timeout: int = Field(
        10, description="Browser navigation timeout in seconds"
    )

    # Allure
    allure_dir: str = Field(
        "reports/allure", description="Directory for Allure results"
    )

    # Database (optional)
    db_host: str = Field("localhost", description="Database host")
    db_port: int = Field(5432, description="Database port")
    db_name: str = Field("test_db", description="Database name")
    db_user: str = Field("test_user", description="Database user")
    db_password: str = Field("test_password", description="Database password")

    model_config = SettingsConfigDict(
        env_file=(".env", ".env.local"),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


def get_settings(env: str | None = None) -> Settings:
    """
    Load settings with optional environment override.

    Args:
        env: Environment name (dev, staging, prod).
             Loads config/environments/{env}.env if provided.

    Returns:
        Configured Settings instance.
    """
    env_files = [".env", ".env.local"]

    if env:
        env_file_path = (
            Path(__file__).parent / "environments" / f"{env}.env"
        )
        if env_file_path.exists():
            env_files.insert(0, str(env_file_path))

    return Settings(_env_file=env_files)
