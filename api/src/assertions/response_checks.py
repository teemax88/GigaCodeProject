from __future__ import annotations

from typing import Any

import allure
import requests
from loguru import logger


class ApiResponseChecks:
    """
    API response checks layer.

    All API assertion logic lives here.
    API clients call these checks after receiving responses.

    Usage:
        response = client.post("/users", json=payload)
        ApiResponseChecks.assert_status_code(response, 201)
        ApiResponseChecks.assert_json_contains(response.json(), {"id": 1})
    """

    @classmethod
    def assert_status_code(cls, response: requests.Response, expected: int) -> None:
        """Assert HTTP status code matches expected."""
        if response.status_code != expected:
            cls._attach_error_response(response)
        assert response.status_code == expected, (
            f"Expected status {expected}, got {response.status_code}. "
            f"Response: {response.text[:500]}"
        )
        logger.info(f"Status code OK: {response.status_code}")

    @classmethod
    def assert_status_in_range(cls, response: requests.Response, start: int, end: int) -> None:
        """Assert HTTP status code is within range."""
        assert start <= response.status_code <= end, (
            f"Expected status in range [{start}, {end}], got {response.status_code}"
        )
        logger.info(f"Status code in range OK: {response.status_code}")

    @classmethod
    def assert_json_field(cls, json_data: dict, field: str, expected: Any) -> None:
        """Assert JSON field has expected value."""
        assert field in json_data, f"Field '{field}' not found in response"
        assert json_data[field] == expected, (
            f"Field '{field}': expected {expected!r}, got {json_data[field]!r}"
        )
        logger.debug(f"Field '{field}' = {expected!r}")

    @classmethod
    def assert_json_field_exists(cls, json_data: dict, field: str) -> None:
        """Assert JSON field exists (not None)."""
        assert field in json_data, f"Field '{field}' not found in response"
        assert json_data[field] is not None, f"Field '{field}' is None"
        logger.debug(f"Field '{field}' exists and is not None")

    @classmethod
    def assert_json_field_type(cls, json_data: dict, field: str, expected_type: type) -> None:
        """Assert JSON field is of expected type."""
        assert field in json_data, f"Field '{field}' not found in response"
        assert isinstance(json_data[field], expected_type), (
            f"Field '{field}': expected {expected_type.__name__}, "
            f"got {type(json_data[field]).__name__}"
        )
        logger.debug(f"Field '{field}' type OK: {type(json_data[field]).__name__}")

    @classmethod
    def assert_json_contains(cls, json_data: dict, expected: dict) -> None:
        """Assert JSON contains expected key-value pairs (recursive)."""
        for key, value in expected.items():
            assert key in json_data, f"Key '{key}' not found"
            if isinstance(value, dict):
                assert isinstance(json_data[key], dict), (
                    f"Key '{key}': expected dict, got {type(json_data[key]).__name__}"
                )
                cls.assert_json_contains(json_data[key], value)
            else:
                assert json_data[key] == value, (
                    f"Key '{key}': expected {value!r}, got {json_data[key]!r}"
                )
        logger.debug("JSON content verified")

    @classmethod
    def assert_json_array_length(
        cls, json_data: dict, field: str, length: int
    ) -> None:
        """Assert JSON array has expected length."""
        assert field in json_data, f"Field '{field}' not found"
        assert isinstance(json_data[field], list), (
            f"Field '{field}': expected list, got {type(json_data[field]).__name__}"
        )
        assert len(json_data[field]) == length, (
            f"Array '{field}': expected length {length}, got {len(json_data[field])}"
        )
        logger.debug(f"Array '{field}' length OK: {length}")

    @classmethod
    def assert_json_field_greater_than(
        cls, json_data: dict, field: str, threshold: float
    ) -> None:
        """Assert numeric field is greater than threshold."""
        cls.assert_json_field_exists(json_data, field)
        assert json_data[field] > threshold, (
            f"Field '{field}': expected > {threshold}, got {json_data[field]}"
        )
        logger.debug(f"Field '{field}' > {threshold}: OK")

    @classmethod
    def assert_response_time_less_than(
        cls, response: requests.Response, max_ms: float
    ) -> None:
        """Assert response time is less than max_ms."""
        elapsed_ms = response.elapsed.total_seconds() * 1000
        assert elapsed_ms < max_ms, (
            f"Response time {elapsed_ms:.1f}ms exceeds limit {max_ms}ms"
        )
        logger.debug(f"Response time OK: {elapsed_ms:.1f}ms < {max_ms}ms")

    @classmethod
    def assert_header(cls, response: requests.Response, name: str, value: str) -> None:
        """Assert response header exists and has expected value."""
        actual = response.headers.get(name)
        assert actual is not None, f"Header '{name}' not found"
        assert actual == value, (
            f"Header '{name}': expected {value!r}, got {actual!r}"
        )
        logger.debug(f"Header '{name}' = {value!r}")

    @classmethod
    def assert_token_valid(cls, json_data: dict) -> str:
        """Assert token exists and return it."""
        cls.assert_json_field_exists(json_data, "access_token")
        token = json_data["access_token"]
        cls.assert_json_field_type(json_data, "access_token", str)
        assert len(token) > 10, "Token seems too short"
        logger.debug("Token valid")
        return token

    @classmethod
    def attach_request(cls, method: str, url: str, body: Any = None) -> None:
        """Attach request info to Allure."""
        allure.attach(f"{method} {url}", name="request", attachment_type=allure.attachment_type.TEXT)
        if body:
            allure.attach(
                str(body), name="request_body", attachment_type=allure.attachment_type.JSON
            )

    @classmethod
    def attach_response(cls, response: requests.Response) -> None:
        """Attach response body to Allure."""
        allure.attach(
            response.text, name="response", attachment_type=allure.attachment_type.TEXT
        )

    @classmethod
    def _attach_error_response(cls, response: requests.Response) -> None:
        """Attach error response details to Allure."""
        allure.attach(
            response.text,
            name="error_response",
            attachment_type=allure.attachment_type.JSON,
        )
        allure.attach(
            f"Expected status: N/A, Got: {response.status_code}",
            name="error_info",
            attachment_type=allure.attachment_type.TEXT,
        )
