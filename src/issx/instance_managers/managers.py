from issx.clients.interfaces import InstanceClientInterface, IssueClientInterface
from issx.domain import SupportedBackend
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

    @classmethod
    def clear_backends(cls) -> None:
        cls.backends.clear()

    def get_instance_client(self, instance: str) -> InstanceClientInterface:
        """
        Get an instance client for a given instance name.

        Converts the instance config to the appropriate config class
         and creates an instance client.
        Args:
            instance: Instance name

        Returns: Instance of an instance client
        """
        instance_config = self.config.get_instance_config(instance)
        client_class = self.backends[instance_config.backend][0]
        instance_config = client_class.instance_config_class(
            **instance_config.raw_config, raw_config=instance_config.raw_config
        )
        return client_class.instance_from_config(instance_config)

    def get_project_client(self, project: str) -> IssueClientInterface:
        """
        Get a project client for a given project name.

        Converts the project config to the appropriate config class
        and creates a project client.
        Args:
            project: Project name

        Returns: Instance of a project client

        """
        project_config = self.config.get_project_config(project)
        instance_config = self.config.get_instance_config(project_config.instance)
        instance_client_class, project_client_class = self.backends[
            instance_config.backend
        ]
        instance_config = instance_client_class.instance_config_class(
            **instance_config.raw_config, raw_config=instance_config.raw_config
        )
        project_config = project_client_class.project_config_class(
            **project_config.raw_config, raw_config=project_config.raw_config
        )
        return project_client_class.from_config(instance_config, project_config)
