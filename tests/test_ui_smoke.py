"""Smoke tests for UI."""

import allure


@allure.epic("Smoke тесты")
@allure.feature("UI Smoke")
class TestUiSmoke:

    @allure.story("Базовая проверка UI")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("smoke")
    @allure.tag("ui")
    def test_ui_configured(self, ui_base_url):
        """Verify UI base URL is configured."""
        assert ui_base_url is not None
        assert len(ui_base_url) > 0
