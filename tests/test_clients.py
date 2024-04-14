import abc
from abc import abstractmethod

import pytest
from issx.clients.exceptions import IssueDoesNotExistError
from issx.clients.interfaces import IssueClientInterface
from issx.domain.issues import Issue

from tests.memory_clients import InMemoryIssueClient


class BaseTestIssueClientInterface(abc.ABC):
    @abstractmethod
    def issue_client(self) -> IssueClientInterface:
        raise NotImplementedError

    @abstractmethod
    def existing_issue(self, issue_client: IssueClientInterface) -> Issue:
        raise NotImplementedError

    @pytest.mark.asyncio
    async def test_create_issue_returns_a_new_instance(
        self, issue_client: IssueClientInterface
    ):
        issue = await issue_client.create_issue("Title", "Description")

        retrieved_issue = await issue_client.get_issue(issue.id)
        assert issue == retrieved_issue

        assert issue.title == "Title"
        assert issue.description == "Description"
        assert issue.web_url == "memory:///issue/1"

    @pytest.mark.asyncio
    async def test_get_issue_raises_issue_does_not_exist_error(self, issue_client):
        with pytest.raises(IssueDoesNotExistError) as exc_info:
            await issue_client.get_issue(1)
        assert exc_info.value.issue_id == 1

    @pytest.mark.asyncio
    async def test_get_issue_returns_an_instance(self, issue_client, existing_issue):
        retrieved_issue = await issue_client.get_issue(existing_issue.id)

        assert existing_issue == retrieved_issue


class TestIssueClientInterface(BaseTestIssueClientInterface):
    @pytest.fixture
    def issue_client(self) -> InMemoryIssueClient:
        return InMemoryIssueClient(
            base_url="memory://",
        )

    @pytest.fixture
    def existing_issue(self, issue_client):
        issue_client.issues[issue_client._current_id] = issue = Issue(
            id=issue_client._current_id,
            title="Title",
            description="Description",
            web_url="memory:///issue/1",
            reference="#1",
        )
        issue_client._current_id += 1
        return issue
