import abc
from typing import ClassVar, Self

from issx.domain.config import InstanceConfig, ProjectFlatConfig
from issx.domain.issues import Issue


class InstanceClientInterface(abc.ABC):
    """
    Interface for a client that interacts with an issue tracker instance
    """

    instance_config_class: ClassVar[type[InstanceConfig]] = InstanceConfig

    @abc.abstractmethod
    async def auth(self) -> str | None:
        """
        Authenticate the client with the instance.
        Raises an internal error if the authentication fails or returns None.
        :return: The username of the authenticated user or None
        """
        pass

    @abc.abstractmethod
    def get_instance_url(self) -> str:
        """
        :return: The URL of the instance
        """
        pass

    @classmethod
    @abc.abstractmethod
    def instance_from_config(cls, instance_config: InstanceConfig) -> Self:
        """
        Create an instance of the client from a configuration dictionary.
        If required, the instance_config can be converted to an instance-specific
        configuration according to the `instance_config_class` attribute of the client.

        :param instance_config: The configuration object. Higher level code
        should validate the configuration.
        :return: An instance of the client
        """
        pass


class IssueClientInterface(abc.ABC):
    project_config_class: ClassVar[type[ProjectFlatConfig]] = ProjectFlatConfig

    @abc.abstractmethod
    async def get_issue(self, issue_id: int) -> Issue:
        """
        Retrieve an issue by its ID.
        Raises IssueDoesNotExistError if the issue does not exist.
        :param issue_id: The ID of the issue
        :return: Issue object
        """
        pass

    @abc.abstractmethod
    async def create_issue(
        self, title: str, description: str, assign_to_me: bool = False
    ) -> Issue:
        """
        Create a new issue.
        :param title: The title of the issue
        :param description: The description of the issue
        :param assign_to_me: Assign the issue to the authenticated user
        :return:
        """
        pass

    @abc.abstractmethod
    async def find_issues(self, title: str) -> list[Issue]:
        """
        Find issues by title using an exact match.
        :param title: The title of the issue
        :return: List of issues
        """
        pass

    @classmethod
    @abc.abstractmethod
    def from_config(
        cls, instance_config: InstanceConfig, project_config: ProjectFlatConfig
    ) -> Self:
        """
        Create an instance of the client from configuration classes.
        If required, the project_config can be converted to a project-specific
        configuration according to the `project_config_class` attribute of the client.

        Args:
            instance_config: InstanceConfig to configure the client to the instance
            project_config: ProjectFlatConfig to configure client. This config can then
            be converted to a project-specific config according to
            the `project_config_class` attribute of the client.
            to the particular project

        Returns:
            An instance of the client

        """
        pass
