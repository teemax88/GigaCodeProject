from __future__ import annotations

from pathlib import Path

from config.api.settings import (
    ApiDevSettings,
    ApiProdSettings,
    ApiSettings,
    ApiStagingSettings,
)
from config.ui.settings import (
    UiDevSettings,
    UiProdSettings,
    UiSettings,
    UiStagingSettings,
)

ENV_MAP = {
    "api": {
        "dev": ApiDevSettings,
        "staging": ApiStagingSettings,
        "prod": ApiProdSettings,
    },
    "ui": {
        "dev": UiDevSettings,
        "staging": UiStagingSettings,
        "prod": UiProdSettings,
    },
}

ENV_DIR = Path(__file__).parent / "environments"


def get_api_settings(env: str = "dev") -> ApiSettings:
    """Load API settings for environment."""
    settings_class = ENV_MAP["api"].get(env, ApiDevSettings)
    return settings_class()


def get_ui_settings(env: str = "dev") -> UiSettings:
    """Load UI settings for environment."""
    settings_class = ENV_MAP["ui"].get(env, UiDevSettings)
    return settings_class()
