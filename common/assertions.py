from __future__ import annotations

import json
from typing import Any

from loguru import logger


class AssertManager:
    """
    Centralized assertion manager with detailed error messages and Allure attachments.

    Usage:
        assert_manager = AssertManager()
        assert_manager.assert_status_code(response, 200)
        assert_manager.assert_response_contains(response.json(), {"key": "value"})
    """

    def assert_status_code(self, response, expected: int, message: str = ""):
        """Assert HTTP status code."""
        if not message:
            message = f"Expected status {expected}, got {response.status_code}"
        assert response.status_code == expected, message
        logger.info(f"Status code OK: {response.status_code}")

    def assert_response_contains(
        self, actual: dict | list, expected: dict, message: str = ""
    ):
        """Assert that actual response contains expected keys/values."""
        if not message:
            message = f"Response should contain: {expected}"
        if isinstance(expected, dict):
            for key, value in expected.items():
                assert key in actual, f"Key '{key}' not found in response"
                if isinstance(value, dict):
                    self.assert_response_contains(actual[key], value, message)
                else:
                    assert actual[key] == value, (
                        f"Key '{key}': expected {value}, got {actual[key]}"
                    )
        logger.info(f"Response content verified")

    def assert_response_field(
        self, response_json: dict, field: str, expected: Any, message: str = ""
    ):
        """Assert specific field value in JSON response."""
        if not message:
            message = f"Field '{field}' should be {expected}"
        assert field in response_json, f"Field '{field}' not found in response"
        assert response_json[field] == expected, (
            f"Field '{field}': expected {expected}, got {response_json[field]}"
        )
        logger.info(f"Field '{field}' = {expected}")

    def assert_not_none(self, value: Any, field_name: str = ""):
        """Assert value is not None."""
        name = field_name or "Value"
        assert value is not None, f"{name} should not be None"
        logger.info(f"{name} is not None")

    def assert_greater_than(
        self, value: float, threshold: float, field_name: str = ""
    ):
        """Assert value is greater than threshold."""
        name = field_name or "Value"
        assert value > threshold, f"{name} {value} should be > {threshold}"
        logger.info(f"{name} {value} > {threshold}")

    def attach_json(self, name: str, data: Any):
        """Attach JSON data to Allure report."""
        allure.attach(
            json.dumps(data, ensure_ascii=False, indent=2, default=str),
            name=name,
            attachment_type=allure.attachment_type.JSON,
        )
        logger.debug(f"Allure attachment '{name}' added")

    def attach_text(self, name: str, text: str):
        """Attach plain text to Allure report."""
        allure.attach(
            text, name=name, attachment_type=allure.attachment_type.TEXT
        )
        logger.debug(f"Allure attachment '{name}' added")
