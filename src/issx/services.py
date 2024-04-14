from issx.clients.interfaces import IssueClientInterface
from issx.domain.issues import Issue


class CopyIssueService:
    def __init__(
        self, source_client: IssueClientInterface, target_client: IssueClientInterface
    ):
        self.source_client = source_client
        self.target_client = target_client

    async def copy(
        self,
        issue_id: int,
        title_format: str = "{title}",
        description_format: str = "{description}",
    ) -> Issue:
        source_issue = await self.source_client.get_issue(issue_id)
        new_issue = await self.target_client.create_issue(
            title=self._prepare_string(source_issue, title_format),
            description=self._prepare_string(source_issue, description_format),
        )
        return new_issue

    @staticmethod
    def _prepare_string(issue: Issue, title_format: str) -> str:
        """
        :param issue: Issue object from which to create the new title
        :param title_format: template string for the new title.
        Can contain placeholders for the issue attributes:
        {id}, {title}, {description}, {web_url}, {reference}
        :return:
        """
        return title_format.format(
            id=issue.id,
            title=issue.title,
            description=issue.description,
            web_url=issue.web_url,
            reference=issue.reference,
        )
