from typing import List
from enum import Enum
import warnings
from .interface import VersionIncrementer, VersionIncrement, Commit
from . import config
from . import errors


class InvalidCommitAction(str, Enum):
    error = 'error'
    warning = 'warning'
    skip = 'skip'


class DefaultIncrementer(VersionIncrementer):
    invalid_commit_action: InvalidCommitAction

    def __init__(
        self,
        invalid_commit_action: InvalidCommitAction = InvalidCommitAction.skip,
    ):
        self.invalid_commit_action = invalid_commit_action

    def get_version_increment(self, commits: List[Commit]) -> VersionIncrement:
        return max(
            (self._commit_to_inc(c) for c in commits), key=lambda vi: vi.value
        )

    def _commit_to_inc(self, commit: Commit) -> VersionIncrement:
        if commit.breaking:
            return VersionIncrement.major
        elif commit.type in config.commit_types_minor:
            return VersionIncrement.minor
        elif commit.type in config.commit_types_patch:
            return VersionIncrement.patch
        elif commit.type in config.commit_types_skip:
            return VersionIncrement.skip

        if self.invalid_commit_action == InvalidCommitAction.error:
            raise errors.InvalidCommitType
        elif self.invalid_commit_action == InvalidCommitAction.warning:
            warnings.warn(f'Invalid commit type {type}')
        else:
            return VersionIncrement.skip
