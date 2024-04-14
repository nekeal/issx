from issx.clients.exceptions import IssueDoesNotExistError
from issx.clients.interfaces import IssueClientInterface
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

    async def create_issue(self, title: str, description: str) -> Issue:
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

    @classmethod
    def from_config(cls, config: dict) -> "InMemoryIssueClient":
        """
        Create an instance of the InMemoryIssueClient from a configuration dictionary.
        :param config: The configuration dictionary. Higher level code should validate
        the configuration.
        :return: An instance of the InMemoryIssueClient
        """
        return cls(
            initial_issues=config.get("initial_issues", []),
            base_url=config.get("base_url", "memory://"),
        )
