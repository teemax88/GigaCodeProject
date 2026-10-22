"""Smoke tests for API."""

import allure

from checks.api.response_checks import ApiResponseChecks


@allure.epic("Smoke тесты")
@allure.feature("API Smoke")
class TestApiSmoke:

    @allure.story("Базовая проверка API")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("smoke")
    @allure.tag("api")
    def test_api_client_initialized(self, api_client):
        """Verify API client is properly initialized."""
        assert api_client is not None
        assert len(api_client.base_url) > 0
