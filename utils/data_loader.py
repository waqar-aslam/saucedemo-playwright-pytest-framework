import copy
import json
import os
from functools import cache
from pathlib import Path
from typing import Any


class JSONDataLoader:
    """Generic JSON loader."""

    @staticmethod
    def load(file_path: str | Path) -> Any:
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"Data file not found: {path}")

        with path.open("r", encoding="utf-8") as file:
            return json.load(file)


@cache
def _read_cached(path: Path) -> Any:
    return JSONDataLoader.load(path)


class DataLoader:
    """Central access point for framework test data.

    Files are read once per session; callers get a fresh copy each time.
    """

    ROOT_DIR = Path(__file__).resolve().parent.parent
    CONFIG_DIR = ROOT_DIR / "config"

    @classmethod
    def _load(cls, file_name: str) -> Any:
        return copy.deepcopy(_read_cached(cls.CONFIG_DIR / file_name))

    @classmethod
    def credentials(cls) -> dict:
        """Users from credentials.json.

        Any value can be overridden with SAUCEDEMO_<USER_KEY>_USERNAME /
        SAUCEDEMO_<USER_KEY>_PASSWORD, e.g. SAUCEDEMO_VALID_USER_PASSWORD.
        """
        users = cls._load("credentials.json")
        for key, user in users.items():
            prefix = f"SAUCEDEMO_{key.upper()}_"
            user["username"] = os.environ.get(prefix + "USERNAME", user["username"])
            user["password"] = os.environ.get(prefix + "PASSWORD", user["password"])
        return users

    @classmethod
    def base_url(cls) -> str:
        return cls._load("urls.json")["base_url"]

    @classmethod
    def test_data(cls) -> dict:
        return cls._load("test_data.json")
