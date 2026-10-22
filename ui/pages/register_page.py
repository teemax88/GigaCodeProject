"""Register page object."""

from __future__ import annotations

from playwright.sync_api import Page

from checks.ui.element_checks import UiElementChecks
from common.base_page import BasePage
from common.decorators import allure_step
from data.locators.auth_locators import AuthLocators


class RegisterPage(BasePage):
    """
    Registration page object.

    Locators from data/locators/auth_locators.py
    """

    PAGE_URL = "/register"
    PAGE_NAME = "Register"

    def __init__(self, page: Page, base_url: str = ""):
        super().__init__(page, base_url)
        self.locators = AuthLocators()

    @allure_step("Открытие страницы регистрации")
    def go_to(self):
        super().go_to()

    @allure_step("Заполнение полей регистрации")
    def fill_registration_form(self, first_name: str, last_name: str, email: str, password: str):
        """Fill all registration fields."""
        self.fill(self.locators.first_name_field, first_name)
        self.fill(self.locators.last_name_field, last_name)
        self.fill(self.locators.email_field, email)
        self.fill(self.locators.password_field, password)
        self.fill(self.locators.confirm_password_field, password)

    @allure_step("Нажатие кнопки регистрации")
    def click_register(self):
        self.click(self.locators.register_button)

    @allure_step("Проверка успешной регистрации")
    def verify_success(self):
        UiElementChecks.assert_visible(self.page, self.locators.success_message)

    @allure_step("Проверка валидации формы")
    def verify_form_error(self, locator: str = ""):
        if locator:
            UiElementChecks.assert_visible(self.page, locator)
        else:
            UiElementChecks.assert_visible(self.page, self.locators.form_validation_error)
