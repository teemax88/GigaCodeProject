from __future__ import annotations

from typing import Any

import allure
import requests
from loguru import logger

from api.src.assertions.response_checks import ApiResponseChecks
from common.decorators import allure_step, log_step


class BaseAPIClient:
    """
    Base API client — only handles HTTP transport.

    All assertion logic is delegated to ApiResponseChecks.

    Usage:
        client = BaseAPIClient(base_url="https://api.example.com")
        response = client.post("/users", json={"name": "John"})
        ApiResponseChecks.assert_status_code(response, 201)
    """

    def __init__(self, base_url: str, timeout: int = 30, headers: dict | None = None):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            **(headers or {}),
        })
        logger.info(f"API Client initialized: {self.base_url}")

    @allure_step("Отправка {method.upper()} запроса к {endpoint}")
    @log_step
    def request(
        self,
        method: str,
        endpoint: str,
        params: dict | None = None,
        json: dict | None = None,
        data: dict | None = None,
        headers: dict | None = None,
        timeout: int | None = None,
    ) -> requests.Response:
        """Send HTTP request with full logging."""
        url = f"{self.base_url}{endpoint}"
        timeout = timeout or self.timeout
        extra_headers = {**(self.session.headers or {}), **(headers or {})}

        # Attach request to Allure
        ApiResponseChecks.attach_request(method, url, json)

        # Log request
        logger.info(f"REQUEST | {method} {url}")
        if params:
            logger.debug(f"  params={params}")
        if json:
            logger.debug(f"  body={json}")

        # Send request
        response = self.session.request(
            method=method.upper(),
            url=url,
            params=params,
            json=json,
            data=data,
            headers=extra_headers,
            timeout=timeout,
        )

        # Log response
        logger.info(
            f"RESPONSE | {method} {url} | status={response.status_code} | time={response.elapsed.total_seconds():.3f}s"
        )
        logger.debug(f"  response_body={response.text[:500]}")

        # Attach response to Allure
        ApiResponseChecks.attach_response(response)

        return response

    def get(self, endpoint: str, **kwargs) -> requests.Response:
        return self.request("GET", endpoint, **kwargs)

    def post(self, endpoint: str, **kwargs) -> requests.Response:
        return self.request("POST", endpoint, **kwargs)

    def put(self, endpoint: str, **kwargs) -> requests.Response:
        return self.request("PUT", endpoint, **kwargs)

    def patch(self, endpoint: str, **kwargs) -> requests.Response:
        return self.request("PATCH", endpoint, **kwargs)

    def delete(self, endpoint: str, **kwargs) -> requests.Response:
        return self.request("DELETE", endpoint, **kwargs)

    def close(self):
        """Close the session."""
        self.session.close()
        logger.info("API Client session closed")

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
