from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Generator

import allure
import pytest
from playwright.sync_api import Browser, Page, Playwright, sync_playwright

# Add project root to sys.path for imports
project_root = Path(__file__).parent.resolve()
sys.path.insert(0, str(project_root))

from config import get_api_settings, get_ui_settings
from config.api.settings import ApiSettings
from config.ui.settings import UiSettings
from logging_config.logger import setup_logger
from common.base_api import BaseAPIClient


# =============================================================================
# Session-scoped settings fixtures
# =============================================================================

@pytest.fixture(scope="session")
def api_env(request) -> str:
    """API environment name from --api-env option."""
    return getattr(request.config, "api_env", "dev")


@pytest.fixture(scope="session")
def ui_env(request) -> str:
    """UI environment name from --ui-env option."""
    return getattr(request.config, "ui_env", "dev")


@pytest.fixture(scope="session")
def api_settings(api_env: str) -> ApiSettings:
    """Load API settings from environment."""
    return get_api_settings(env=api_env)


@pytest.fixture(scope="session")
def ui_settings(ui_env: str) -> UiSettings:
    """Load UI settings from environment."""
    return get_ui_settings(env=ui_env)


@pytest.fixture(scope="session")
def logger(api_settings: ApiSettings, ui_settings: UiSettings):
    """Initialize logger for the test session."""
    return setup_logger()


# =============================================================================
# API fixtures
# =============================================================================

@pytest.fixture(scope="session")
def api_base_url(api_settings: ApiSettings) -> str:
    """API base URL from settings."""
    return api_settings.base_url


@pytest.fixture(scope="session")
def api_timeout(api_settings: ApiSettings) -> int:
    """API request timeout from settings."""
    return api_settings.timeout


@pytest.fixture(scope="session")
def api_client(api_settings: ApiSettings) -> Generator[BaseAPIClient, None, None]:
    """
    Session-scoped API client.
    Automatically closed after all tests.
    """
    client = BaseAPIClient(
        base_url=api_settings.base_url,
        timeout=api_settings.timeout,
        headers=api_settings.default_headers,
    )
    yield client
    client.close()


# =============================================================================
# Browser fixtures
# =============================================================================

@pytest.fixture(scope="session")
def browser_context_args(ui_settings: UiSettings):
    """Configure browser context for all tests."""
    return {
        "headless": ui_settings.headless,
        "viewport": {
            "width": ui_settings.viewport_width,
            "height": ui_settings.viewport_height,
        },
        "ignore_https_errors": True,
        "locale": "en-US",
        "timezone_id": "Europe/Moscow",
        "slow_mo": ui_settings.slow_mo,
    }


@pytest.fixture(scope="session")
def playwright_instance() -> Generator[Playwright, None, None]:
    """Launch Playwright instance for the session."""
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="session")
def browser(playwright_instance: Playwright, ui_settings: UiSettings) -> Generator[Browser, None, None]:
    """Launch browser for the session."""
    browser = getattr(playwright_instance, ui_settings.browser).launch(
        headless=ui_settings.headless,
        slow_mo=ui_settings.slow_mo,
    )
    yield browser
    browser.close()


# =============================================================================
# Page fixtures
# =============================================================================

@pytest.fixture(scope="function")
def page(browser, logger) -> Generator[Page, None, None]:
    """
    Create a new page for each test.
    Takes screenshot on failure.
    """
    context = browser.new_context()
    page = context.new_page()

    # Attach console logs
    page.on("console", lambda msg: logger.debug(f"CONSOLE | {msg.text}"))
    page.on("pageerror", lambda err: logger.error(f"PAGE_ERROR | {err}"))

    yield page

    # Screenshot on failure
    if pytest.config._opfailed:
        screenshot_path = f"reports/logs/failed_{pytest.config._test_number}.png"
        page.screenshot(path=screenshot_path, full_page=True)
        logger.error(f"Screenshot saved: {screenshot_path}")

    context.close()


@pytest.fixture(scope="function")
def ui_base_url(ui_settings: UiSettings) -> str:
    """UI base URL from settings."""
    return ui_settings.base_url


# =============================================================================
# Test data fixtures
# =============================================================================

@pytest.fixture
def generated_user():
    """Generate random user data."""
    from common.helpers.generators import DataGenerator
    return DataGenerator.user_payload()


@pytest.fixture
def generated_email():
    """Generate random email."""
    from common.helpers.generators import DataGenerator
    return DataGenerator.email()


@pytest.fixture
def generated_username():
    """Generate random username."""
    from common.helpers.generators import DataGenerator
    return DataGenerator.username()


# =============================================================================
# Pytest hooks
# =============================================================================

pytest.config._test_number = 0
pytest.config._opfailed = False


def pytest_runtest_makereport(item, call):
    """Hook to capture test status for screenshots."""
    if call.when == "call" and call.excinfo is not None:
        pytest.config._opfailed = True
    else:
        pytest.config._opfailed = False


def pytest_runtest_setup(item):
    """Increment test counter."""
    pytest.config._test_number += 1


def pytest_configure(config):
    """Register custom markers and options."""
    config.addinivalue_line("markers", "smoke: smoke-тесты")
    config.addinivalue_line("markers", "regression: регрессионные тесты")
    config.addinivalue_line("markers", "api: API-тесты")
    config.addinivalue_line("markers", "ui: UI-тесты")
    config.addinivalue_line("markers", "slow: медленные тесты")

    config.addoption(
        "--api-env",
        default="dev",
        help="API environment (dev, staging, prod)",
    )
    config.addoption(
        "--ui-env",
        default="dev",
        help="UI environment (dev, staging, prod)",
    )
