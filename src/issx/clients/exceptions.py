class EntityDoesNotExistError(Exception):
    pass


class IssueDoesNotExistError(EntityDoesNotExistError):
    pass


class ProjectDoesNotExistError(EntityDoesNotExistError):
    pass
