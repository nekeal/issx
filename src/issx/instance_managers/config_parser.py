import tomllib
from pathlib import Path
from typing import Self

import attr
from attr import define, field

from issx.domain import SupportedBackend
from issx.domain.config import InstanceConfig, ProjectFlatConfig


@define
class GenericConfig:
    instances: dict[str, InstanceConfig]
    projects: dict[str, ProjectFlatConfig] = field()

    @projects.validator
    def validate_projects(
        self, attribute: attr.Attribute, value: dict[str, ProjectFlatConfig]
    ) -> None:
        for project in value.values():
            if project.instance not in self.instances:
                raise ValueError(f"Instance {project.instance} not found")


class GenericConfigParser:
    def __init__(self, data: GenericConfig):
        self._data: GenericConfig = data

    def get_instance_config(self, instance: str) -> InstanceConfig:
        return self._data.instances[instance]

    def get_project_config(self, project: str) -> ProjectFlatConfig:
        return self._data.projects[project]

    @classmethod
    def from_file(cls, config_file: Path | None = None) -> Self:
        config_file = config_file or cls._find_config_file()
        return cls.from_dict(tomllib.loads(config_file.read_text()))

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        parsed_data = GenericConfig(
            instances={
                name: InstanceConfig(
                    backend=SupportedBackend(instance.get("backend")),
                    url=instance.get("url"),
                    token=instance.get("token"),
                    raw_config=instance,
                )
                for name, instance in data["instances"].items()
            },
            projects={
                name: ProjectFlatConfig(
                    instance=project.get("instance"),
                    project=project.get("project"),
                    raw_config=project,
                )
                for name, project in data.get("projects", {}).items()
            },
        )
        return cls(parsed_data)

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
