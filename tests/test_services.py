import pytest
import pytest_asyncio
from issx.clients.interfaces import IssueClientInterface
from issx.domain.issues import Issue
from issx.services import CopyIssueService

from tests.memory_clients import InMemoryIssueClient


class TestCopyIssueService:
    @pytest.fixture
    def client_1(self):
        return InMemoryIssueClient(
            base_url="memory://client1",
        )

    @pytest.fixture
    def client_2(self):
        return InMemoryIssueClient(
            base_url="memory://client2",
        )

    @pytest_asyncio.fixture
    async def issue(self, client_1: IssueClientInterface) -> Issue:
        return await client_1.create_issue("Title", "Description")

    @pytest.mark.asyncio
    async def test_copy_returns_copied_issue(self, client_1, client_2, issue: Issue):
        service = CopyIssueService(client_1, client_2)

        copied_issue = await service.copy(issue.id)

        assert copied_issue != issue

        assert copied_issue.title == issue.title
        assert copied_issue.description == issue.description
        assert copied_issue.web_url == "memory://client2/issue/1"

    @pytest.mark.asyncio
    async def test_copy_issue_is_saved(
        self,
        client_1: IssueClientInterface,
        client_2: IssueClientInterface,
        issue: Issue,
    ):
        service = CopyIssueService(client_1, client_2)

        copied_issue = await service.copy(issue.id)

        assert await client_2.get_issue(copied_issue.id) == copied_issue
