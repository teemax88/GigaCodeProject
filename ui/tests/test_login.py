"""Example UI tests for login page."""

from __future__ import annotations

import allure

from checks.ui.element_checks import UiElementChecks
from ui.pages.login_page import LoginPage
from ui.pages.dashboard_page import DashboardPage


@allure.epic("Авторизация UI")
@allure.feature("Login Page")
class TestLoginUI:

    @allure.story("Успешный вход в систему")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("ui")
    @allure.tag("smoke")
    def test_login_success(self, page, ui_base_url, generated_user):
        """Test successful login through UI."""
        login_page = LoginPage(page, ui_base_url)

        # Navigate and fill
        login_page.go_to()
        login_page.fill_username(generated_user["username"])
        login_page.fill_password(generated_user["password"])
        login_page.click_login()

        # Verify dashboard loaded (checks layer)
        dashboard = DashboardPage(page, ui_base_url)
        dashboard.verify_loaded()

    @allure.story("Неудачный вход")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.tag("ui")
    def test_login_invalid_credentials(self, page, ui_base_url):
        """Test login with invalid credentials."""
        login_page = LoginPage(page, ui_base_url)

        login_page.go_to()
        login_page.fill_username("invalid_user")
        login_page.fill_password("wrong_password")
        login_page.click_login()

        # Check error via checks layer
        login_page.verify_error_visible("Invalid")
