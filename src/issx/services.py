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
        allow_duplicates: bool = False,
        assign_to_me: bool = False,
    ) -> Issue:
        """
        Copy an issue from the source client to the target client optionally
        applying a title and description format. If allow_duplicates is False,
        the method will return a first issue found with the same title.

        :param issue_id: The ID of the issue to copy
        :param title_format: The format for the new issue title
        :param description_format: The format for the new issue description
        :param allow_duplicates: Whether to allow duplicate issues
        :param assign_to_me: Whether to assign the new issue to the current user
        :return: Newly created or existing issue in the target client
        """
        source_issue = await self.source_client.get_issue(issue_id)
        target_title = self._prepare_string(source_issue, title_format)
        if not allow_duplicates and (
            issues := await self.target_client.find_issues(target_title)
        ):
            return issues[0]
        new_issue = await self.target_client.create_issue(
            title=target_title,
            description=self._prepare_string(source_issue, description_format),
            assign_to_me=assign_to_me,
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
