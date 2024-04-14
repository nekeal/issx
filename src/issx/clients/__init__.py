from enum import StrEnum

__all__ = ["SupportedBackend", "GitlabClient"]

from issx.clients.gitlab import GitlabClient


class SupportedBackend(StrEnum):
    gitlab = "gitlab"
    redmine = "redmine"
