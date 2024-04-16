import tomllib
from pathlib import Path
from typing import Any

from issx.clients import SupportedBackend
from issx.clients.interfaces import InstanceClientInterface, IssueClientInterface


class GenericConfigParser:
    def __init__(self, config_file: Path | None = None):
        self.config_file = config_file or self._find_config_file()
        self._data: dict[str, dict[str, dict]] = tomllib.loads(
            self.config_file.read_text()
        )

    def get_instance_config(self, instance: str) -> dict:
        return self._data["instances"][instance]

    def get_project_config(self, project: str) -> dict:
        return self._data["projects"][project]

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
    backends: dict[
        SupportedBackend,
        tuple[type[InstanceClientInterface], type[IssueClientInterface]],
    ] = {}

    def __init__(self, config: GenericConfigParser):
        self.config = config

    @classmethod
    def register_backend(
        cls,
        backend: SupportedBackend,
        instance_client_class: type[InstanceClientInterface],
        project_client_class: type[IssueClientInterface],
    ) -> None:
        cls.backends[backend] = (instance_client_class, project_client_class)

    def get_instance_client(self, instance: str) -> InstanceClientInterface:
        instance_config = self.config.get_instance_config(instance)
        backend = SupportedBackend(instance_config["backend"])
        client_class = self.backends[backend][0]
        return client_class.from_config(instance_config)

    def get_project_client(self, project: str) -> IssueClientInterface:
        project_config = self.config.get_project_config(project)
        instance_config = self.config.get_instance_config(project_config["instance"])
        project_config["instance"] = instance_config
        backend = SupportedBackend(instance_config["backend"])
        client_class = self.backends[backend][1]
        return client_class.from_config(project_config)
