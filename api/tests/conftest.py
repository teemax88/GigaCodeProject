"""API test fixtures."""

from __future__ import annotations

from typing import Generator

import pytest

from api.src.clients.auth_client import AuthClient
from api.src.clients.user_client import UserClient
from common.base_api import BaseAPIClient
from common.helpers.generators import DataGenerator


# =============================================================================
# API Client fixtures
# =============================================================================

@pytest.fixture(scope="module")
def auth_client(api_client: BaseAPIClient) -> AuthClient:
    """Module-scoped AuthClient."""
    return AuthClient(
        base_url=api_client.base_url,
        timeout=api_client.timeout,
    )


@pytest.fixture(scope="module")
def user_client(api_client: BaseAPIClient) -> UserClient:
    """Module-scoped UserClient."""
    return UserClient(
        base_url=api_client.base_url,
        timeout=api_client.timeout,
    )


# =============================================================================
# Test data fixtures
# =============================================================================

@pytest.fixture
def generated_user() -> dict:
    """Generate random user data."""
    return DataGenerator.user_payload()


@pytest.fixture
def generated_email() -> str:
    """Generate random email."""
    return DataGenerator.email()


@pytest.fixture
def generated_username() -> str:
    """Generate random username."""
    return DataGenerator.username()


@pytest.fixture
def registered_user(auth_client: AuthClient, generated_user: dict) -> Generator[dict, None, None]:
    """Register a user and return it for teardown."""
    auth_client.register(generated_user)
    yield generated_user
