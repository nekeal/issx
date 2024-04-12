from pathlib import Path
from typing import Any

import tomllib

from issx.clients import SupportedBackend
from issx.clients.interfaces import InstanceClientInterface


class GenericConfigParser:
    def __init__(self, config_file: Path | None = None):
        self.config_file = config_file or self._find_config_file()
        self._data: dict[str, dict[str, dict]] = tomllib.loads(
            self.config_file.read_text()
        )

    def get_instance_config(self, instance: str) -> dict:
        return self._data["instances"][instance]

    def __getitem__(self, item: str) -> Any:
        return self._data[item]

    @staticmethod
    def _find_config_file() -> Path:
        locations = [
            Path("issx.toml"),
            Path("~/.config/issx.toml").expanduser(),
        ]
        for location in locations:
            if location.exists() and location.is_file() and location.suffix == ".toml":
                return location
        raise FileNotFoundError("No configuration file found")


class InstanceManager:
    backends: dict[SupportedBackend, type[InstanceClientInterface]] = {}

    def __init__(self, config: GenericConfigParser):
        self.config = config

    @classmethod
    def register_backend(
        cls, backend: SupportedBackend, client_class: type[InstanceClientInterface]
    ) -> None:
        cls.backends[backend] = client_class

    def get_instance_client(self, instance: str) -> InstanceClientInterface:
        instance_config = self.config.get_instance_config(instance)
        backend = SupportedBackend(instance_config["backend"])
        client_class = self.backends[backend]
        return client_class.from_config(instance_config)
