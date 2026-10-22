from __future__ import annotations

import logging
from functools import wraps
from typing import Any, Callable

import allure
from loguru import logger as loguru_logger


def get_logger(name: str) -> logging.Logger:
    """
    Create a standard logging.Logger instance.

    Args:
        name: Logger name (usually __name__).

    Returns:
        Configured logging.Logger.
    """
    log = logging.getLogger(name)
    if not log.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        log.addHandler(handler)
        log.setLevel(logging.DEBUG)
    return log


def log_step(func: Callable) -> Callable:
    """
    Decorator that logs function entry/exit and captures arguments.

    Usage:
        @log_step
        def my_step(arg1, arg2):
            ...
    """
    func_name = func.__qualname__

    @wraps(func)
    def wrapper(*args, **kwargs):
        loguru_logger.debug(f"ENTER | {func_name} | args={args}, kwargs={kwargs}")
        try:
            result = func(*args, **kwargs)
            loguru_logger.debug(f"EXIT  | {func_name} | result={result}")
            return result
        except Exception as e:
            loguru_logger.error(f"ERROR | {func_name} | exception={e}")
            raise

    return wrapper


def allure_step(name: str):
    """
    Decorator that wraps a function in an Allure step and logs it.

    Usage:
        @allure_step("Login as user")
        def login(username, password):
            ...
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        @allure.step(name)
        @log_step
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    return decorator
