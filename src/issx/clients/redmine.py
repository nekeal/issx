from typing import Self

from redminelib import Redmine
from redminelib.exceptions import ResourceNotFoundError
from redminelib.resources import Issue as RedmineIssue
from redminelib.resources import Project
from redminelib.resultsets import ResourceSet

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

    @classmethod
    def issues_to_domain_list(cls, issues: ResourceSet) -> list[Issue]:  # type: ignore[no-any-unimported]
        return [cls.issue_to_domain(issue) for issue in issues]


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

    async def create_issue(
        self, title: str, description: str, assign_to_me: bool = False
    ) -> Issue:
        issue = self.client.issue.create(
            project_id=(await self.get_project()).id,
            subject=title,
            description=description,
            assigned_to_id="me" if assign_to_me else None,
        )
        return RedmineIssueMapper.issue_to_domain(issue)

    async def get_issue(self, issue_id: int) -> Issue:
        try:
            issue = self.client.issue.get(issue_id)
        except ResourceNotFoundError as e:
            raise IssueDoesNotExistError(issue_id) from e
        return RedmineIssueMapper.issue_to_domain(issue)

    async def find_issues(self, title: str) -> list[Issue]:
        return RedmineIssueMapper.issues_to_domain_list(
            self.client.issue.filter(
                project_id=(await self.get_project()).id, subject=title
            )
        )

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
