from issx.clients.exceptions import IssueDoesNotExistError
from issx.clients.interfaces import IssueClientInterface
from issx.domain.config import InstanceConfig, ProjectFlatConfig
from issx.domain.issues import Issue


class InMemoryIssueClient(IssueClientInterface):
    def __init__(
        self, initial_issues: list[Issue] | None = None, base_url: str = "memory://"
    ):
        """
        Initialize the InMemoryIssueClient with an
        empty dictionary of issues and a _current_id of 1.
        """
        self.issues = (
            {issue.id: issue for issue in initial_issues} if initial_issues else {}
        )
        self._current_id = max(self.issues.keys(), default=0) + 1
        self._base_url = base_url

    async def get_issue(self, issue_id: int) -> Issue:
        if issue := self.issues.get(issue_id):
            return issue
        raise IssueDoesNotExistError(issue_id)

    async def create_issue(
        self, title: str, description: str, assign_to_me: bool = False
    ) -> Issue:
        issue = Issue(
            id=self._current_id,
            title=title,
            description=description,
            web_url=f"{self._base_url}/issue/{self._current_id}",
            reference=f"#{self._current_id}",
        )
        self.issues[self._current_id] = issue
        self._current_id += 1
        return issue

    async def find_issues(self, title: str) -> list[Issue]:
        return [issue for issue in self.issues.values() if issue.title == title]

    @classmethod
    def from_config(
        cls, instance_config: InstanceConfig, project_config: ProjectFlatConfig
    ) -> "InMemoryIssueClient":
        """
        Create an instance of the client from a configuration classes
        """
        return cls()
