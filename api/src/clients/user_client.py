"""User management API client."""

from __future__ import annotations

from typing import Any

import allure
from requests import Response

from api.src.assertions.response_checks import ApiResponseChecks
from common.base_api import BaseAPIClient
from common.decorators import allure_step


class UserClient(BaseAPIClient):
    """
    User management API client.

    Uses ApiResponseChecks for validation.
    """

    @allure_step("Создание пользователя")
    def create_user(self, payload: dict[str, Any]) -> Response:
        """Create a new user and validate response."""
        response = self.post("/users", json=payload)
        ApiResponseChecks.assert_status_code(response, 201)
        ApiResponseChecks.assert_json_field_exists(response.json(), "id")
        return response

    @allure_step("Получение списка пользователей")
    def get_users(self, page: int = 1, limit: int = 20) -> Response:
        """Get list of users."""
        params = {"page": page, "limit": limit}
        response = self.get("/users", params=params)
        ApiResponseChecks.assert_status_code(response, 200)
        ApiResponseChecks.assert_json_field_type(response.json(), "data", list)
        return response

    @allure_step("Получение пользователя по ID")
    def get_user(self, user_id: int | str) -> Response:
        """Get user by ID."""
        response = self.get(f"/users/{user_id}")
        ApiResponseChecks.assert_status_code(response, 200)
        ApiResponseChecks.assert_json_field_exists(response.json(), "id")
        return response

    @allure_step("Обновление пользователя")
    def update_user(self, user_id: int | str, payload: dict[str, Any]) -> Response:
        """Update user."""
        response = self.put(f"/users/{user_id}", json=payload)
        ApiResponseChecks.assert_status_code(response, 200)
        return response

    @allure_step("Удаление пользователя")
    def delete_user(self, user_id: int | str) -> Response:
        """Delete user."""
        response = self.delete(f"/users/{user_id}")
        ApiResponseChecks.assert_status_code(response, 204)
        return response

    @allure_step("Поиск пользователей")
    def search_users(self, query: str) -> Response:
        """Search users by query."""
        params = {"query": query}
        response = self.get("/users/search", params=params)
        ApiResponseChecks.assert_status_code(response, 200)
        ApiResponseChecks.assert_json_field_type(response.json(), "results", list)
        return response
