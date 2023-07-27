import re
from semv.interface import RawCommit, Commit, CommitParser


class AngularCommitParser(CommitParser):
    def __init__(self):
        self.type_and_scope_pattern = re.compile(
            r'(?P<type>\w+)\((?P<scope>\w+)\): .*'
        )
        self.breaking_pattern = re.compile(
            r'BREAKING CHANGE: .*', flags=re.DOTALL
        )

    def parse(self, commit: RawCommit) -> Commit:
        m = self.type_and_scope_pattern.match(commit.title)
        type = m.group('type')
        scope = m.group('scope')
        n = self.breaking_pattern.match(commit.body)
        breaking = bool(n)
        return Commit(
            sha=commit.sha, type=type, scope=scope, breaking=breaking
        )
