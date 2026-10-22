from __future__ import annotations

from playwright.sync_api import Page, expect

from common.decorators import allure_step, log_step


class BasePage:
    """
    Base page object — only handles browser actions.

    All assertions are delegated to UiElementChecks.

    Usage:
        class LoginPage(BasePage):
            def login(self, username, password):
                self.fill("#username", username)
                self.fill("#password", password)
                self.click('button[type="submit"]')

        # In tests:
        login_page.login("user", "pass")
        UiElementChecks.assert_visible(page, "#dashboard")
    """

    PAGE_URL: str = ""
    PAGE_NAME: str = "BasePage"

    def __init__(self, page: Page, base_url: str = ""):
        self.page = page
        self.base_url = base_url.rstrip("/")

    @allure_step("Переход на страницу")
    @log_step
    def go_to(self, path: str | None = None):
        """Navigate to page."""
        url = f"{self.base_url}{path}" if path else (
            f"{self.base_url}{self.PAGE_URL}" if self.PAGE_URL else self.base_url
        )
        self.page.goto(url, timeout=self._timeout * 1000)
        self.page.wait_for_load_state("networkidle")

    @allure_step("Ожидание загрузки страницы")
    @log_step
    def wait_for_load(self, state: str = "load"):
        """Wait for page state."""
        self.page.wait_for_load_state(state)

    @allure_step("Ожидание видимости элемента")
    @log_step
    def wait_for_visible(self, locator: str, timeout: int | None = None):
        """Wait for element to be visible."""
        timeout = timeout or self._timeout
        expect(self.page.locator(locator)).to_be_visible(timeout=timeout * 1000)

    @allure_step("Ожидание невидимости элемента")
    @log_step
    def wait_for_hidden(self, locator: str, timeout: int | None = None):
        """Wait for element to be hidden."""
        timeout = timeout or self._timeout
        expect(self.page.locator(locator)).to_be_hidden(timeout=timeout * 1000)

    @allure_step("Ожидание наличия элемента")
    @log_step
    def wait_for_present(self, locator: str, timeout: int | None = None):
        """Wait for element to be present in DOM."""
        timeout = timeout or self._timeout
        expect(self.page.locator(locator)).to_be_attached(timeout=timeout * 1000)

    @allure_step("Ожидание текста элемента")
    @log_step
    def wait_for_text(self, locator: str, text: str, timeout: int | None = None):
        """Wait for element to contain text."""
        timeout = timeout or self._timeout
        expect(self.page.locator(locator)).to_have_text(text, timeout=timeout * 1000)

    @allure_step("Нажатие на элемент")
    @log_step
    def click(self, locator: str, timeout: int | None = None):
        """Click element."""
        timeout = timeout or self._timeout
        self.page.locator(locator).click(timeout=timeout * 1000)

    @allure_step("Нажатие с ожиданием видимости")
    @log_step
    def click_visible(self, locator: str, timeout: int | None = None):
        """Wait for visible then click."""
        timeout = timeout or self._timeout
        expect(self.page.locator(locator)).to_be_visible(timeout=timeout * 1000)
        self.page.locator(locator).click()

    @allure_step("Ввод текста в элемент")
    @log_step
    def fill(self, locator: str, text: str, timeout: int | None = None):
        """Fill input field."""
        timeout = timeout or self._timeout
        self.page.locator(locator).fill(text, timeout=timeout * 1000)

    @allure_step("Очистка поля ввода")
    @log_step
    def clear(self, locator: str, timeout: int | None = None):
        """Clear input field."""
        timeout = timeout or self._timeout
        self.page.locator(locator).clear(timeout=timeout * 1000)

    @allure_step("Добавление текста к существующему")
    @log_step
    def type(self, locator: str, text: str, timeout: int | None = None):
        """Type text into field (appends)."""
        timeout = timeout or self._timeout
        self.page.locator(locator).type(text, timeout=timeout * 1000)

    @allure_step("Получение текста элемента")
    @log_step
    def get_text(self, locator: str) -> str:
        """Get text content of element."""
        return self.page.locator(locator).text_content()

    @allure_step("Получение значения атрибута")
    @log_step
    def get_attribute(self, locator: str, attr: str) -> str | None:
        """Get attribute value of element."""
        return self.page.locator(locator).get_attribute(attr)

    @allure_step("Проверка видимости элемента")
    @log_step
    def is_visible(self, locator: str) -> bool:
        """Check if element is visible."""
        return self.page.locator(locator).is_visible()

    @allure_step("Проверка наличия элемента")
    @log_step
    def is_present(self, locator: str) -> bool:
        """Check if element exists in DOM."""
        return self.page.locator(locator).is_attached()

    @allure_step("Выбор опции в select")
    @log_step
    def select_option(self, locator: str, value: str):
        """Select option in dropdown."""
        self.page.locator(locator).select_option(value)

    @allure_step("Скриншот страницы")
    @log_step
    def screenshot(self, name: str = "page_screenshot") -> bytes:
        """Take screenshot of the page."""
        return self.page.screenshot(full_page=True)

    @allure_step("Получение текущей URL")
    @log_step
    def get_current_url(self) -> str:
        """Get current page URL."""
        return self.page.url

    @allure_step("Обновление страницы")
    @log_step
    def reload(self):
        """Reload current page."""
        self.page.reload()

    @property
    def _timeout(self) -> int:
        """Default timeout in seconds."""
        return 10

    def __repr__(self):
        return f"<{self.__class__.__name__} url={self.base_url}{self.PAGE_URL}>"
