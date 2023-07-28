from dataclasses import dataclass, replace
from enum import Enum


class InvalidCommitAction(str, Enum):
    error = 'error'
    warning = 'warning'
    skip = 'skip'


@dataclass
class RawCommit:
    sha: str
    title: str
    body: str


@dataclass
class Commit:
    sha: str
    type: str
    scope: str
    breaking: bool


class VersionIncrement(str, Enum):
    # NOTE: The values here are alphabetically sorted. This is used downstream
    skip = 'skip'
    patch = 'patch'
    minor = 'minor'
    major = 'major'


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
        if inc == VersionIncrement.skip:
            return self
        elif inc == VersionIncrement.major:
            return replace(self, major=self.major+1, minor=0, patch=0)
        elif inc == VersionIncrement.minor:
            return replace(self, minor=self.minor+1, patch=0)
        elif inc == VersionIncrement.patch:
            return replace(self, patch=self.patch+1)
        raise RuntimeError('This should never happen')
