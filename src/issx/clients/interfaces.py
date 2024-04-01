import abc

from issx.domain.issues import Issue


class IssueClientInterface(abc.ABC):
    @abc.abstractmethod
    async def get_issue(self, issue_id: int) -> Issue:
        pass

    @abc.abstractmethod
    async def create_issue(self, title: str, description: str) -> Issue:
        pass
