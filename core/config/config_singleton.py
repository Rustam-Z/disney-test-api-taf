from __future__ import annotations
from pathlib import Path
from threading import Lock

import yaml
from munch import DefaultMunch


def _get_config(path: str | Path) -> dict:
    with open(path) as file:
        return yaml.safe_load(file)


class SingletonMeta(type):
    _instances = {}
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class ConfigSingleton(metaclass=SingletonMeta):
    def __init__(self, config_file_path: str | Path):
        self.config_file_path = config_file_path
        self._config = DefaultMunch.fromDict(_get_config(self.config_file_path))

    def get_config(self):
        return self._config
