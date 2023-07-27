from typing import Iterator
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
    def get_version_increment(
        self, commits: Iterator[Commit]
    ) -> VersionIncrement:
        pass
