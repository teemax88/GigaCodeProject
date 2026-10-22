"""Login page object."""

from __future__ import annotations

from playwright.sync_api import Page

from checks.ui.element_checks import UiElementChecks
from common.base_page import BasePage
from common.decorators import allure_step
from data.locators.auth_locators import AuthLocators


class LoginPage(BasePage):
    """
    Login page object.

    Locators are imported from data/locators/auth_locators.py
    Assertions are delegated to UiElementChecks.
    """

    PAGE_URL = "/login"
    PAGE_NAME = "Login"

    def __init__(self, page: Page, base_url: str = ""):
        super().__init__(page, base_url)
        self.locators = AuthLocators()

    @allure_step("Открытие страницы логина")
    def go_to(self):
        """Navigate to login page."""
        super().go_to()

    @allure_step("Ввод имени пользователя: {username}")
    def fill_username(self, username: str):
        """Fill username field."""
        self.fill(self.locators.username_field, username)

    @allure_step("Ввод пароля")
    def fill_password(self, password: str):
        """Fill password field."""
        self.fill(self.locators.password_field, password)

    @allure_step("Нажатие кнопки входа")
    def click_login(self):
        """Click login button."""
        self.click(self.locators.login_button)

    @allure_step("Проверка отображения страницы логина")
    def verify_page_loaded(self):
        """Verify login page is loaded."""
        UiElementChecks.assert_visible(self.page, self.locators.login_page_title)

    @allure_step("Проверка ошибки входа")
    def verify_error_visible(self, expected_text: str = ""):
        """Verify error message is displayed."""
        UiElementChecks.assert_visible(self.page, self.locators.error_message)
        if expected_text:
            UiElementChecks.assert_text(self.page, self.locators.error_message, expected_text)

    @allure_step("Проверка отсутствия ошибки")
    def verify_error_hidden(self):
        """Verify error message is hidden."""
        UiElementChecks.assert_hidden(self.page, self.locators.error_message)

    @allure_step("Проверка видимости ссылки регистрации")
    def verify_register_link_visible(self):
        """Verify register link is visible."""
        UiElementChecks.assert_visible(self.page, self.locators.register_link)

    @allure_step("Переход на страницу регистрации")
    def go_to_register(self):
        """Navigate to register page."""
        self.click(self.locators.register_link)
