from __future__ import annotations

import json
from typing import Any

from loguru import logger


class JsonUtils:
    """Utility methods for JSON operations."""

    @staticmethod
    def load_json(filepath: str) -> dict | list:
        """Load JSON from file."""
        logger.debug(f"Loading JSON from: {filepath}")
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        logger.debug(f"JSON loaded: {type(data).__name__}")
        return data

    @staticmethod
    def save_json(filepath: str, data: dict | list) -> None:
        """Save data to JSON file."""
        logger.debug(f"Saving JSON to: {filepath}")
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        logger.debug("JSON saved successfully")

    @staticmethod
    def merge_dicts(base: dict, override: dict) -> dict:
        """Deep merge two dictionaries. Override values take precedence."""
        result = base.copy()
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = JsonUtils.merge_dicts(result[key], value)
            else:
                result[key] = value
        return result

    @staticmethod
    def flatten_dict(d: dict, parent_key: str = "", sep: str = ".") -> dict:
        """Flatten a nested dictionary."""
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(JsonUtils.flatten_dict(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)


class FileHelper:
    """Utility methods for file operations."""

    @staticmethod
    def read_text(filepath: str, encoding: str = "utf-8") -> str:
        """Read text file."""
        logger.debug(f"Reading text file: {filepath}")
        with open(filepath, "r", encoding=encoding) as f:
            return f.read()

    @staticmethod
    def write_text(filepath: str, content: str, encoding: str = "utf-8") -> None:
        """Write text to file."""
        logger.debug(f"Writing text to: {filepath}")
        with open(filepath, "w", encoding=encoding) as f:
            f.write(content)
