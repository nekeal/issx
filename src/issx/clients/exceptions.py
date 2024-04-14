class EntityDoesNotExistError(Exception):
    pass


class IssueDoesNotExistError(EntityDoesNotExistError):
    def __init__(self, issue_id: int):
        self.issue_id = issue_id
        super().__init__(f"Issue with id={issue_id} does not exist")


class ProjectDoesNotExistError(EntityDoesNotExistError):
    pass
