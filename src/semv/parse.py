from typing import Optional
import re
import sys
from .interface import RawCommit, Commit, CommitParser
from . import errors
from .types import InvalidCommitAction
from .utils import warn_or_raise


class AngularCommitParser(CommitParser):
    def __init__(
        self,
        invalid_commit_action: InvalidCommitAction = InvalidCommitAction.skip,
    ):
        self.type_and_scope_pattern = re.compile(
            r'(?P<type>\w+)\((?P<scope>\w+)\): .*'
        )
        self.breaking_pattern = re.compile(
            r'BREAKING CHANGE: .*', flags=re.DOTALL
        )
        self.invalid_commit_action = invalid_commit_action

    def parse(self, commit: RawCommit) -> Optional[Commit]:
        m = self.type_and_scope_pattern.match(commit.title)
        if m is None:
            warn_or_raise(
                f'Invalid commit: {commit.sha} {commit.title}',
                self.invalid_commit_action,
                errors.InvalidCommitFormat,
            )
            return None
        type = m.group('type')
        scope = m.group('scope')
        n = self.breaking_pattern.match(commit.body)
        breaking = bool(n)
        return Commit(
            sha=commit.sha, type=type, scope=scope, breaking=breaking
        )
