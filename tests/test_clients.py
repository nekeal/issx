import abc
import asyncio
import os
import uuid
from abc import abstractmethod
from collections.abc import AsyncGenerator

import pytest
import pytest_asyncio
from gitlab import Gitlab
from issx.clients import GitlabClient
from issx.clients.exceptions import IssueDoesNotExistError
from issx.clients.interfaces import IssueClientInterface
from issx.clients.redmine import RedmineClient
from issx.domain.issues import Issue
from redminelib import Redmine

from tests.memory_clients import InMemoryIssueClient


class BaseTestIssueClientInterface(abc.ABC):
    pytestmark = pytest.mark.skipif(
        not os.environ.get("ISSX_TEST_INTEGRATION"), reason="Integration tests disabled"
    )
    config: dict

    @abstractmethod
    def issue_client(self) -> IssueClientInterface:
        raise NotImplementedError

    @abstractmethod
    async def existing_issue(self, issue_client: IssueClientInterface) -> Issue:
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
        assert str(issue.id) in issue.web_url

    @pytest.mark.asyncio
    async def test_get_issue_raises_issue_does_not_exist_error(self, issue_client):
        with pytest.raises(IssueDoesNotExistError) as exc_info:
            await issue_client.get_issue(-1)
        assert exc_info.value.issue_id == -1

    @pytest.mark.asyncio
    async def test_get_issue_returns_an_instance(self, issue_client, existing_issue):
        retrieved_issue = await issue_client.get_issue(existing_issue.id)

        assert existing_issue == retrieved_issue

    @pytest.mark.asyncio
    async def test_get_non_existent_issue_raises_error(self, issue_client):
        with pytest.raises(IssueDoesNotExistError):
            await issue_client.get_issue(-1)

    @pytest.mark.asyncio
    async def test_find_issues_returns_a_list_of_issues(self, issue_client):
        title1, title2 = str(uuid.uuid4()), str(uuid.uuid4())
        async with asyncio.TaskGroup() as g:
            issue1_task = g.create_task(
                issue_client.create_issue(title1, "Description 1")
            )
            g.create_task(issue_client.create_issue(title2, "Description 2"))

        issues = await issue_client.find_issues(title1)

        assert len(issues) == 1
        assert issues[0].title == title1
        assert issues[0].id == issue1_task.result().id


class TestIssueClientInterface(BaseTestIssueClientInterface):
    pytestmark = pytest.mark.skipif(False, reason="Integration tests disabled")

    @pytest_asyncio.fixture
    def issue_client(self) -> InMemoryIssueClient:
        return InMemoryIssueClient(
            base_url="memory://",
        )

    @pytest_asyncio.fixture
    async def existing_issue(self, issue_client):
        issue_client.issues[issue_client._current_id] = issue = Issue(
            id=issue_client._current_id,
            title="Title",
            description="Description",
            web_url="memory:///issue/1",
            reference="#1",
        )
        issue_client._current_id += 1
        return issue


class TestRedmineIssueClientInterface(BaseTestIssueClientInterface):
    config: dict

    @classmethod
    def setup_class(cls):
        cls.config = cls.get_config()

    @pytest.fixture
    def issue_client(self) -> RedmineClient:
        return RedmineClient(
            client=Redmine(
                os.environ["ISSX_TEST_REDMINE_HOST"],
                key=os.environ["ISSX_TEST_REDMINE_TOKEN"],
            ),
            project_id=int(os.environ["ISSX_TEST_REDMINE_PROJECT_ID"]),
        )

    @pytest_asyncio.fixture
    async def existing_issue(self, issue_client) -> AsyncGenerator[Issue, None]:
        yield (
            issue := await issue_client.create_issue(
                title=str(uuid.uuid4()),
                description=f"Description {uuid.uuid4()}",
            )
        )
        issue_client.client.issue.delete(issue.id)

    @staticmethod
    def get_config():
        try:
            return {
                "url": os.environ["ISSX_TEST_REDMINE_HOST"],
                "token": os.environ["ISSX_TEST_REDMINE_TOKEN"],
                "project_id": int(os.environ["ISSX_TEST_REDMINE_PROJECT_ID"]),
            }
        except KeyError as e:
            pytest.skip(f"Skipping Redmine tests due to missing configuration {e}")


class TestGitlabIssueClientInterface(BaseTestIssueClientInterface):
    @classmethod
    def setup_class(cls):
        cls.config = cls.get_config()

    @pytest.fixture
    def issue_client(self) -> GitlabClient:
        return GitlabClient(
            client=Gitlab(self.config["url"], private_token=self.config["token"]),
            project_id=self.config["project_id"],
        )

    @pytest_asyncio.fixture
    async def existing_issue(self, issue_client) -> AsyncGenerator[Issue, None]:
        yield (
            issue := await issue_client.create_issue(
                title=str(uuid.uuid4()),
                description=f"Description {uuid.uuid4()}",
            )
        )
        issue_client._project.issues.delete(issue.id)

    @staticmethod
    def get_config():
        try:
            return {
                "url": os.environ["ISSX_TEST_GITLAB_HOST"],
                "token": os.environ["ISSX_TEST_GITLAB_TOKEN"],
                "project_id": int(os.environ["ISSX_TEST_GITLAB_PROJECT_ID"]),
            }
        except KeyError as e:
            pytest.skip(f"Skipping Gitlab tests due to missing configuration {e}")
