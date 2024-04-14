from typing import Self

from redminelib import Redmine
from redminelib.exceptions import ResourceNotFoundError
from redminelib.resources import Issue as RedmineIssue
from redminelib.resources import Project

from issx.clients.exceptions import IssueDoesNotExistError, ProjectDoesNotExistError
from issx.clients.interfaces import InstanceClientInterface, IssueClientInterface
from issx.domain.issues import Issue


class RedmineIssueMapper:
    """
    Maps Redmine API objects to domain objects
    """

    @classmethod
    def issue_to_domain(cls, issue: RedmineIssue) -> Issue:  # type: ignore[no-any-unimported]
        return Issue(
            id=issue.id,
            title=issue.subject,
            description=issue.description,
            web_url=issue.url,
            reference=issue.id,
        )


class RedmineInstanceClient(InstanceClientInterface):
    def __init__(self, client: Redmine):  # type: ignore[no-any-unimported]
        self.client = client

    async def auth(self) -> str | None:
        return str(self.client.auth())

    def get_instance_url(self) -> str:
        return str(self.client.url)

    @classmethod
    def from_config(cls, config: dict) -> Self:
        return cls(
            Redmine(
                config["url"],
                key=config["token"],
            )
        )


class RedmineClient(IssueClientInterface, RedmineInstanceClient):
    def __init__(self, client: Redmine, project_id: int):  # type: ignore[no-any-unimported]
        self._project_id = project_id
        self._project: Project | None = None  # type: ignore[no-any-unimported]
        super().__init__(client)

    async def create_issue(self, title: str, description: str) -> Issue:
        issue = self.client.issue.create(
            project_id=(await self.get_project()).id,
            subject=title,
            description=description,
        )
        return RedmineIssueMapper.issue_to_domain(issue)

    async def get_issue(self, issue_id: int) -> Issue:
        try:
            issue = self.client.issue.get(issue_id)
        except ResourceNotFoundError as e:
            raise IssueDoesNotExistError(
                f"Issue with id={issue_id} does not exist"
            ) from e
        return RedmineIssueMapper.issue_to_domain(issue)

    async def get_project(self) -> Project:  # type: ignore[no-any-unimported]
        if self._project is None:
            try:
                self._project = self.client.project.get(self._project_id)
            except ResourceNotFoundError as e:
                raise ProjectDoesNotExistError(
                    f"Project with id={self._project_id} does not exist"
                ) from e
        return self._project

    @classmethod
    def from_config(cls, config: dict) -> Self:
        return cls(
            RedmineInstanceClient.from_config(config["instance"]).client,
            project_id=int(config["project"]),
        )
