from typing import Callable, List
from abc import ABC, abstractmethod
import sys
from operator import attrgetter
from .types import Version, VersionIncrement


class VersionEstimator(ABC):
    @abstractmethod
    def run(self, current_version: Version):
        raise NotImplementedError


class Hooks:
    checks: List[VersionEstimator]

    def __init__(self):
        self.checks = []

    def estimate_version_increment(
        self, current_version: Version
    ) -> VersionIncrement:
        check_results = (check.run(current_version) for check in self.checks)
        return VersionIncrement(
            min(
                (x for x in check_results),
                key=attrgetter('value'),
                default=VersionIncrement.skip,
            )
        )

    def register(self, check: VersionEstimator):
        self.checks.append(check)


class DummyVersionEstimator(VersionEstimator):
    increment: VersionIncrement

    def __init__(self, increment: str):
        self.increment = VersionIncrement(increment)

    def run(
        self,
        current_version: Version,
    ) -> VersionIncrement:
        sys.stderr.write(
            f'Dummy version estimator called on version {current_version},'
            f' increment {self.increment}\n'
        )
        return self.increment
