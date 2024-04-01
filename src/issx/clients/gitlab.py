from typing import cast

from gitlab import Gitlab, GitlabGetError
from gitlab.v4.objects import Project, ProjectIssue

from issx.clients.interfaces import IssueClientInterface
from issx.domain.issues import Issue


class EntityDoesNotExistError(Exception):
    pass


class IssueDoesNotExistError(EntityDoesNotExistError):
    pass


class ProjectDoesNotExistError(EntityDoesNotExistError):
    pass


class IssueMapper:
    """
    Maps Gitlab API objects to domain objects
    """

    @classmethod
    def issue_to_domain(cls, issue: ProjectIssue) -> Issue:
        return Issue(
            id=issue.id,
            title=issue.title,
            description=issue.description,
            web_url=issue.web_url,
            reference=issue.references["full"],
        )


class GitlabClient(IssueClientInterface):
    def __init__(self, client: Gitlab, project_id: int):
        self.client = client
        self.project_id = project_id
        self._project: Project | None = None

    async def create_issue(self, title: str, description: str) -> Issue:
        project = await self._get_project()
        issue: ProjectIssue = cast(
            ProjectIssue,
            project.issues.create({"title": title, "description": description}),
        )
        return IssueMapper.issue_to_domain(issue)

    async def get_issue(self, issue_id: int) -> Issue:
        issue: ProjectIssue = await self._get_issue(issue_id)
        return IssueMapper.issue_to_domain(issue)

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
            raise IssueDoesNotExistError(
                f"Issue with id={issue_id} does not exist"
            ) from e
