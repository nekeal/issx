import abc
from typing import Self

from issx.domain.issues import Issue


class InstanceClientInterface(abc.ABC):
    """
    Interface for a client that interacts with an issue tracker instance
    """

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
    def from_config(cls, config: dict) -> Self:
        """
        Create an instance of the client from a configuration dictionary.
        :param config: The configuration dictionary. Higher level code should validate
        the configuration.
        :return: An instance of the client
        """
        pass


class IssueClientInterface(abc.ABC):
    @abc.abstractmethod
    async def get_issue(self, issue_id: int) -> Issue:
        pass

    @abc.abstractmethod
    async def create_issue(self, title: str, description: str) -> Issue:
        pass

    @classmethod
    @abc.abstractmethod
    def from_config(cls, config: dict) -> Self:
        pass
