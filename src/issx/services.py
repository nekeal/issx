from issx.clients.interfaces import IssueClientInterface
from issx.domain.issues import Issue


class CopyIssueService:
    def __init__(
        self, source_client: IssueClientInterface, target_client: IssueClientInterface
    ):
        self.source_client = source_client
        self.target_client = target_client

    async def copy(self, issue_id: int) -> Issue:
        source_issue = await self.source_client.get_issue(issue_id)
        new_issue = await self.target_client.create_issue(
            source_issue.title, source_issue.description
        )
        return new_issue
