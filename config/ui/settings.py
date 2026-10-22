from __future__ import annotations

from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class UiSettings(BaseSettings):
    """UI environment configuration."""

    base_url: str = Field(
        ..., description="Base URL for UI application"
    )
    browser: Literal["chrome", "firefox", "webkit"] = Field(
        "chrome", description="Browser to use for UI tests"
    )
    headless: bool = Field(
        False, description="Run browser in headless mode"
    )
    viewport_width: int = Field(
        1920, description="Browser viewport width"
    )
    viewport_height: int = Field(
        1080, description="Browser viewport height"
    )
    navigation_timeout: int = Field(
        30000, description="Page navigation timeout in ms"
    )
    action_timeout: int = Field(
        10000, description="Action timeout in ms"
    )
    slow_mo: int = Field(
        0, description="Slow motion in ms (for debugging)"
    )

    model_config = SettingsConfigDict(
        env_prefix="UI_",
        env_file=(".env", ".env.local"),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


class UiDevSettings(UiSettings):
    """UI development environment."""

    base_url: str = "http://localhost:3000"
    headless: bool = False
    slow_mo: int = 500


class UiStagingSettings(UiSettings):
    """UI staging environment."""

    base_url: str = "https://staging.example.com"
    headless: bool = True


class UiProdSettings(UiSettings):
    """UI production environment."""

    base_url: str = "https://example.com"
    headless: bool = True
