from typing import Iterator, List
from abc import ABC, abstractmethod

from .types import Version, RawCommit, Commit, VersionIncrement


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
