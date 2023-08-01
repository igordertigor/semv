from typing import Iterator, Set
import sys
from .interface import VersionIncrementer
from . import errors
from .types import VersionIncrement, Commit, InvalidCommitAction
from .utils import warn_or_raise


class DefaultIncrementer(VersionIncrementer):
    invalid_commit_action: InvalidCommitAction
    commit_types_minor: Set[str]
    commit_types_patch: Set[str]
    commit_types_skip: Set[str]

    def __init__(
        self,
        commit_types_minor,
        commit_types_patch,
        commit_types_skip,
        invalid_commit_action: InvalidCommitAction = InvalidCommitAction.skip,
    ):
        self.commit_types_minor = commit_types_minor
        self.commit_types_patch = commit_types_patch
        self.commit_types_skip = commit_types_skip
        self.invalid_commit_action = invalid_commit_action

    def get_version_increment(
        self, commits: Iterator[Commit]
    ) -> VersionIncrement:
        return min(
            (self._commit_to_inc(c) for c in commits), key=lambda vi: vi.value
        )

    def _commit_to_inc(self, commit: Commit) -> VersionIncrement:
        if commit.breaking:
            return VersionIncrement.major
        elif commit.type in self.commit_types_minor:
            return VersionIncrement.minor
        elif commit.type in self.commit_types_patch:
            return VersionIncrement.patch
        elif commit.type in self.commit_types_skip:
            return VersionIncrement.skip

        warn_or_raise(
            f'Commit {commit.sha} has invalid type {commit.type}',
            self.invalid_commit_action,
            errors.InvalidCommitType,
        )
        return VersionIncrement.skip
