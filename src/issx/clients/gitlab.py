from typing import Self, cast

from gitlab import Gitlab, GitlabGetError
from gitlab.v4.objects import CurrentUser, Project, ProjectIssue

from issx.clients.exceptions import IssueDoesNotExistError, ProjectDoesNotExistError
from issx.clients.interfaces import InstanceClientInterface, IssueClientInterface
from issx.domain.issues import Issue


class IssueMapper:
    """
    Maps Gitlab API objects to domain objects
    """

    @classmethod
    def issue_to_domain(cls, issue: ProjectIssue) -> Issue:
        return Issue(
            id=issue.iid,
            title=issue.title,
            description=issue.description,
            web_url=issue.web_url,
            reference=issue.references["full"],
        )

    @classmethod
    def issues_to_domain_list(cls, issues: list[ProjectIssue]) -> list[Issue]:
        return [cls.issue_to_domain(issue) for issue in issues]


class GitlabInstanceClient(InstanceClientInterface):
    @classmethod
    def from_config(cls, config: dict) -> Self:
        return cls(Gitlab(config["url"], private_token=config["token"]))

    def __init__(self, client: Gitlab):
        self.client = client

    async def auth(self) -> str | None:
        self.client.auth()
        if user := self.client.user:
            return cast(str, user.username)
        return None

    def get_user(self) -> CurrentUser:
        self.client.auth()
        if not self.client.user:
            raise ValueError("Cannot get user from Gitlab client")
        return self.client.user

    def get_instance_url(self) -> str:
        return self.client.url


class GitlabClient(IssueClientInterface, GitlabInstanceClient):
    def __init__(self, client: Gitlab, project_id: int):
        self.project_id = project_id
        self._project: Project | None = None
        super().__init__(client)

    async def create_issue(
        self, title: str, description: str, assign_to_me: bool = False
    ) -> Issue:
        project = await self._get_project()
        issue: ProjectIssue = cast(
            ProjectIssue,
            project.issues.create(
                {
                    "title": title,
                    "description": description,
                    "assignee_id": self.get_user().id,
                }
            ),
        )
        return IssueMapper.issue_to_domain(issue)

    async def get_issue(self, issue_id: int) -> Issue:
        issue: ProjectIssue = await self._get_issue(issue_id)
        return IssueMapper.issue_to_domain(issue)

    async def find_issues(self, title: str) -> list[Issue]:
        project = await self._get_project()
        issues = cast(list[ProjectIssue], list(project.issues.list(search=title)))
        return IssueMapper.issues_to_domain_list(issues)

    async def _get_project(self) -> Project:
        if self._project is None:
            try:
                self._project = self.client.projects.get(self.project_id)
            except GitlabGetError as e:
                raise ProjectDoesNotExistError(
                    f"Project with id={self.project_id} does not exist"
                ) from e
        return self._project

    async def _get_issue(self, issue_id: int) -> ProjectIssue:
        project = await self._get_project()
        try:
            return project.issues.get(issue_id)
        except GitlabGetError as e:
            raise IssueDoesNotExistError(issue_id) from e

    @classmethod
    def from_config(cls, config: dict) -> Self:
        return cls(
            GitlabInstanceClient.from_config(config["instance"]).client,
            project_id=int(config["project"]),
        )
