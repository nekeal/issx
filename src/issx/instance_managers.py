import tomllib
from pathlib import Path
from typing import Self

import attr
from attrs import asdict, define, field

from issx.clients import SupportedBackend
from issx.clients.interfaces import InstanceClientInterface, IssueClientInterface


@define
class InstanceConfig:
    backend: SupportedBackend = attr.ib(validator=attr.validators.in_(SupportedBackend))
    url: str = attr.ib(validator=attr.validators.instance_of(str))
    token: str = attr.ib(validator=attr.validators.instance_of(str))


@define
class ProjectFlatConfig:
    instance: str = attr.ib(validator=attr.validators.instance_of(str))
    project: str = attr.ib(validator=attr.validators.instance_of(str))


@define
class GenericConfig:
    instances: dict[str, InstanceConfig]
    projects: dict[str, ProjectFlatConfig] = field()

    @projects.validator
    def check_projects(
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
                )
                for name, instance in data["instances"].items()
            },
            projects={
                name: ProjectFlatConfig(
                    instance=project.get("instance"),
                    project=project.get("project"),
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
        client_class = self.backends[instance_config.backend][0]
        return client_class.from_config(asdict(instance_config))

    def get_project_client(self, project: str) -> IssueClientInterface:
        project_config = self.config.get_project_config(project)
        instance_config = self.config.get_instance_config(project_config.instance)
        project_config_dict = asdict(project_config)
        project_config_dict["instance"] = asdict(instance_config)
        client_class = self.backends[instance_config.backend][1]
        return client_class.from_config(project_config_dict)
