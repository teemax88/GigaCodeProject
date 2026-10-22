"""Dashboard page object."""

from __future__ import annotations

from playwright.sync_api import Page

from checks.ui.element_checks import UiElementChecks
from common.base_page import BasePage
from common.decorators import allure_step
from data.locators.dashboard_locators import DashboardLocators


class DashboardPage(BasePage):
    """
    Dashboard page object.

    Locators from data/locators/dashboard_locators.py
    """

    PAGE_URL = "/dashboard"
    PAGE_NAME = "Dashboard"

    def __init__(self, page: Page, base_url: str = ""):
        super().__init__(page, base_url)
        self.locators = DashboardLocators()

    @allure_step("Открытие дашборда")
    def go_to(self):
        super().go_to()

    @allure_step("Проверка загрузки дашборда")
    def verify_loaded(self):
        UiElementChecks.assert_visible(self.page, self.locators.dashboard_title)
        UiElementChecks.assert_visible(self.page, self.locators.welcome_message)

    @allure_step("Получение количества статистических карточек")
    def get_stats_count(self) -> int:
        return self.page.locator(self.locators.stats_card).count()

    @allure_step("Проверка видимости активности")
    def verify_activity_visible(self):
        UiElementChecks.assert_visible(self.page, self.locators.activity_list)

    @allure_step("Получение последнего элемента активности")
    def get_last_activity_text(self) -> str | None:
        items = self.page.locator(self.locators.activity_item)
        count = items.count()
        if count > 0:
            return items.last.text_content()
        return None
