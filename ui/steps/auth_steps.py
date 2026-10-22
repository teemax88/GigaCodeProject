"""UI steps for authentication."""

from __future__ import annotations

from playwright.sync_api import Page

from checks.ui.element_checks import UiElementChecks
from common.decorators import allure_step
from ui.pages.login_page import LoginPage
from ui.pages.register_page import RegisterPage


class AuthSteps:
    """
    Authentication scenario steps.

    Uses LoginPage/RegisterPage for actions,
    UiElementChecks for assertions.
    """

    def __init__(self, page: Page):
        self.page = page
        self.login_page = LoginPage(page)
        self.register_page = RegisterPage(page)

    @allure_step("Открытие страницы логина")
    def open_login_page(self):
        self.login_page.go_to()

    @allure_step("Ввод имени пользователя: {username}")
    def enter_username(self, username: str):
        self.login_page.fill_username(username)

    @allure_step("Ввод пароля")
    def enter_password(self, password: str):
        self.login_page.fill_password(password)

    @allure_step("Нажатие кнопки входа")
    def click_login_button(self):
        self.login_page.click_login()

    @allure_step("Проверка успешного входа на дашборд")
    def verify_login_success(self):
        from ui.pages.dashboard_page import DashboardPage
        dashboard = DashboardPage(self.page, self.login_page.base_url)
        dashboard.verify_loaded()

    @allure_step("Проверка ошибки входа: {expected_text}")
    def verify_login_error(self, expected_text: str = ""):
        self.login_page.verify_error_visible(expected_text)

    @allure_step("Регистрация нового пользователя")
    def register_user(self, first_name: str, last_name: str, email: str, password: str):
        self.register_page.go_to()
        self.register_page.fill_registration_form(first_name, last_name, email, password)
        self.register_page.click_register()
        self.register_page.verify_success()
