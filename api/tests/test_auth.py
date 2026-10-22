"""Example API tests for authentication."""

from __future__ import annotations

import allure

from api.clients.auth_client import AuthClient
from checks.api.response_checks import ApiResponseChecks


@allure.epic("Авторизация")
@allure.feature("Auth API")
class TestAuthAPI:

    @allure.story("Успешная регистрация")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("api")
    @allure.tag("smoke")
    def test_register_success(self, api_client, generated_user):
        """Test successful user registration."""
        client = AuthClient(
            base_url=api_client.base_url,
            timeout=api_client.timeout,
        )

        response = client.register(generated_user)
        json_data = response.json()

        # Checks layer validation
        ApiResponseChecks.assert_json_field(json_data, "username", generated_user["username"])
        ApiResponseChecks.assert_json_field(json_data, "email", generated_user["email"])

    @allure.story("Успешная авторизация")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("api")
    @allure.tag("smoke")
    def test_login_success(self, api_client, generated_user):
        """Test successful login."""
        client = AuthClient(
            base_url=api_client.base_url,
            timeout=api_client.timeout,
        )

        # Register first
        client.register(generated_user)

        # Login
        token = client.login_and_get_token(
            generated_user["username"],
            generated_user["password"],
        )

        # Token is already validated inside login_and_get_token
        assert len(token) > 10

    @allure.story("Неудачная авторизация")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.tag("api")
    def test_login_invalid_credentials(self, api_client):
        """Test login with invalid credentials."""
        client = AuthClient(
            base_url=api_client.base_url,
            timeout=api_client.timeout,
        )

        response = client.login("invalid_user", "wrong_password")

        ApiResponseChecks.assert_status_code(response, 401)
