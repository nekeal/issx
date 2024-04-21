from attrs import asdict

from issx.clients.interfaces import InstanceClientInterface, IssueClientInterface
from issx.instance_managers import SupportedBackend
from issx.instance_managers.config_parser import GenericConfigParser


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
