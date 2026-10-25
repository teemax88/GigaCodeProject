"""Authentication API client."""

from __future__ import annotations

from typing import Any

import allure
from requests import Response

from api.src.assertions.response_checks import ApiResponseChecks
from common.base_api import BaseAPIClient
from common.decorators import allure_step


class AuthClient(BaseAPIClient):
    """
    Authentication API client.

    Uses ApiResponseChecks for validation.
    """

    @allure_step("Регистрация нового пользователя")
    def register(self, payload: dict[str, Any]) -> Response:
        """Register a new user and validate response."""
        response = self.post("/auth/register", json=payload)
        ApiResponseChecks.assert_status_code(response, 201)
        ApiResponseChecks.assert_json_field_exists(response.json(), "id")
        ApiResponseChecks.assert_json_field_exists(response.json(), "username")
        return response

    @allure_step("Авторизация пользователя")
    def login(self, username: str, password: str) -> Response:
        """Login and get access token."""
        payload = {"username": username, "password": password}
        response = self.post("/auth/login", json=payload)
        ApiResponseChecks.assert_status_code(response, 200)
        return response

    @allure_step("Получение токена и проверка валидности")
    def login_and_get_token(self, username: str, password: str) -> str:
        """Login and return validated access token."""
        response = self.login(username, password)
        token = ApiResponseChecks.assert_token_valid(response.json())
        return token

    @allure_step("Обновление токена доступа")
    def refresh_token(self, refresh_token: str) -> Response:
        """Refresh access token."""
        payload = {"refresh_token": refresh_token}
        response = self.post("/auth/refresh", json=payload)
        ApiResponseChecks.assert_status_code(response, 200)
        return response

    @allure_step("Выход из системы")
    def logout(self, token: str) -> Response:
        """Logout user."""
        headers = {"Authorization": f"Bearer {token}"}
        response = self.post("/auth/logout", headers=headers)
        ApiResponseChecks.assert_status_code(response, 204)
        return response
