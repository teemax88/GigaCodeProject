from __future__ import annotations

from playwright.sync_api import Page, expect

from loguru import logger


class UiElementChecks:
    """
    UI element checks layer.

    All UI assertion logic lives here.
    Page Objects and Steps call these checks.

    Usage:
        UiElementChecks.assert_visible(page, "#username")
        UiElementChecks.assert_text(page, ".error", "Invalid credentials")
    """

    @classmethod
    def assert_visible(cls, page: Page, locator: str, timeout: int = 10000) -> None:
        """Assert element is visible."""
        try:
            expect(page.locator(locator)).to_be_visible(timeout=timeout)
            logger.debug(f"Element visible: {locator}")
        except Exception as e:
            cls._attach_page_state(page, locator)
            raise AssertionError(f"Element not visible: {locator}") from e

    @classmethod
    def assert_hidden(cls, page: Page, locator: str, timeout: int = 10000) -> None:
        """Assert element is hidden."""
        try:
            expect(page.locator(locator)).to_be_hidden(timeout=timeout)
            logger.debug(f"Element hidden: {locator}")
        except Exception as e:
            cls._attach_page_state(page, locator)
            raise AssertionError(f"Element is not hidden: {locator}") from e

    @classmethod
    def assert_not_present(cls, page: Page, locator: str, timeout: int = 5000) -> None:
        """Assert element is not in DOM."""
        try:
            expect(page.locator(locator)).to_be_attached(timeout=timeout, is_not=True)
            logger.debug(f"Element not present: {locator}")
        except Exception as e:
            raise AssertionError(f"Element is present (should not be): {locator}") from e

    @classmethod
    def assert_text(cls, page: Page, locator: str, expected: str) -> None:
        """Assert element contains expected text."""
        actual = page.locator(locator).text_content()
        assert actual is not None, f"Element text is None: {locator}"
        assert expected in actual, (
            f"Text mismatch for '{locator}': expected '{expected}' in '{actual}'"
        )
        logger.debug(f"Text OK for '{locator}': '{actual.strip()}'")

    @classmethod
    def assert_exact_text(cls, page: Page, locator: str, expected: str) -> None:
        """Assert element has exact text."""
        actual = page.locator(locator).text_content()
        assert actual is not None, f"Element text is None: {locator}"
        assert actual.strip() == expected.strip(), (
            f"Text mismatch for '{locator}': expected '{expected}', got '{actual.strip()}'"
        )
        logger.debug(f"Exact text OK for '{locator}': '{actual.strip()}'")

    @classmethod
    def assert_attribute(
        cls, page: Page, locator: str, attr: str, expected: str
    ) -> None:
        """Assert element attribute has expected value."""
        actual = page.locator(locator).get_attribute(attr)
        assert actual is not None, f"Attribute '{attr}' not found on '{locator}'"
        assert actual == expected, (
            f"Attribute '{attr}' mismatch: expected '{expected}', got '{actual}'"
        )
        logger.debug(f"Attribute '{attr}' OK: '{actual}'")

    @classmethod
    def assert_input_value(cls, page: Page, locator: str, expected: str) -> None:
        """Assert input field has expected value."""
        actual = page.locator(locator).input_value()
        assert actual == expected, (
            f"Input value mismatch for '{locator}': expected '{expected}', got '{actual}'"
        )
        logger.debug(f"Input value OK for '{locator}': '{actual}'")

    @classmethod
    def assert_checked(cls, page: Page, locator: str) -> None:
        """Assert checkbox is checked."""
        is_checked = page.locator(locator).is_checked()
        assert is_checked, f"Checkbox is not checked: {locator}"
        logger.debug(f"Checkbox checked: {locator}")

    @classmethod
    def assert_not_checked(cls, page: Page, locator: str) -> None:
        """Assert checkbox is not checked."""
        is_checked = page.locator(locator).is_checked()
        assert not is_checked, f"Checkbox is checked (should not be): {locator}"
        logger.debug(f"Checkbox not checked: {locator}")

    @classmethod
    def assert_url_contains(cls, page: Page, expected: str) -> None:
        """Assert current URL contains expected string."""
        actual = page.url
        assert expected in actual, (
            f"URL mismatch: expected '{expected}' in '{actual}'"
        )
        logger.debug(f"URL OK: '{actual}'")

    @classmethod
    def assert_url_exact(cls, page: Page, expected: str) -> None:
        """Assert current URL exactly matches expected."""
        actual = page.url
        assert actual == expected, (
            f"URL mismatch: expected '{expected}', got '{actual}'"
        )
        logger.debug(f"URL exact OK: '{actual}'")

    @classmethod
    def assert_title_contains(cls, page: Page, expected: str) -> None:
        """Assert page title contains expected string."""
        actual = page.title()
        assert expected in actual, (
            f"Title mismatch: expected '{expected}' in '{actual}'"
        )
        logger.debug(f"Title OK: '{actual}'")

    @classmethod
    def assert_count(cls, page: Page, locator: str, expected: int) -> None:
        """Assert element count matches expected."""
        count = page.locator(locator).count()
        assert count == expected, (
            f"Element count mismatch for '{locator}': expected {expected}, got {count}"
        )
        logger.debug(f"Element count OK for '{locator}': {count}")

    @classmethod
    def assert_disabled(cls, page: Page, locator: str) -> None:
        """Assert element is disabled."""
        is_disabled = page.locator(locator).is_disabled()
        assert is_disabled, f"Element is not disabled: {locator}"
        logger.debug(f"Element disabled: {locator}")

    @classmethod
    def assert_enabled(cls, page: Page, locator: str) -> None:
        """Assert element is enabled."""
        is_enabled = page.locator(locator).is_enabled()
        assert is_enabled, f"Element is not enabled: {locator}"
        logger.debug(f"Element enabled: {locator}")

    @classmethod
    def assert_dialog_text(cls, page: Page, expected: str, timeout: int = 5000) -> str:
        """Wait for and return dialog text."""
        def handle_dialog(dialog):
            dialog.accept()
            return dialog.message

        dialog_message = page.wait_for_event(
            "dialog", lambda d: True, timeout=timeout
        )
        text = dialog_message.message
        assert expected in text, (
            f"Dialog text mismatch: expected '{expected}' in '{text}'"
        )
        logger.debug(f"Dialog text OK: '{text}'")
        return text

    @classmethod
    def _attach_page_state(cls, page: Page, context_locator: str = "") -> None:
        """Attach page state for debugging on assertion failure."""
        import allure

        allure.attach(
            page.url, name="current_url", attachment_type=allure.attachment_type.TEXT
        )
        allure.attach(
            page.title(), name="page_title", attachment_type=allure.attachment_type.TEXT
        )
        screenshot = page.screenshot(full_page=True)
        allure.attach(
            screenshot, name="page_screenshot", attachment_type=allure.attachment_type.PNG
        )
        if context_locator:
            allure.attach(
                f"Failed locator: {context_locator}",
                name="failed_locator",
                attachment_type=allure.attachment_type.TEXT,
            )
