from typing import Iterator, List
from abc import ABC, abstractmethod
from enum import Enum
from dataclasses import dataclass, replace


@dataclass
class RawCommit:
    sha: str
    message: str


@dataclass
class Commit:
    sha: str
    type: str
    scope: str
    breaking: bool


class VersionIncrement(str, Enum):
    major = 'major'
    minor = 'minor'
    patch = 'patch'


@dataclass
class Version:
    major: int = 1
    minor: int = 0
    patch: int = 0

    @classmethod
    def from_string(cls, s: str):
        if s[0] == 'v':
            s = s[1:]
        else:
            raise ValueError(f'Invalid version string {s}')

        major, minor, patch = [int(x) for x in s.split('.')]
        return cls(major=major, minor=minor, patch=patch)

    def __str__(self):
        return f'v{self.major}.{self.minor}.{self.patch}'

    def __add__(self, inc: VersionIncrement) -> 'Version':
        kw = {inc.value: getattr(self, inc.value) + 1}
        return replace(self, **kw)


class VersionControlSystem(ABC):
    @abstractmethod
    def get_current_version(self) -> Version:
        pass

    @abstractmethod
    def get_commits_without(
        self, current_version: Version
    ) -> Iterator[RawCommit]:
        pass


class CommitParser(ABC):
    @abstractmethod
    def parse(self, commit: RawCommit) -> Commit:
        pass


class VersionIncrementer(ABC):
    @abstractmethod
    def get_version_increment(self, commits: List[Commit]) -> VersionIncrement:
        pass


if __name__ == '__main__':
    # This is just to check that the interface is complete
    vcs = VersionControlSystem()
    cp = CommitParser()
    vi = VersionIncrementer()
    current_version = vcs.get_current_version()
    commits = [cp.parse(c) for c in vcs.get_commits_without(current_version)]
    new_version = current_version + vi.get_version_increment(commits)
