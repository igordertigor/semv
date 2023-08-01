from typing import Callable, List
import sys
from operator import attrgetter
from .types import Version, VersionIncrement

VersionEstimator = Callable[[Version], VersionIncrement]


class Hooks:
    checks: List[VersionEstimator]

    def __init__(self):
        self.checks = []

    def estimate_version_increment(
        self, current_version: Version
    ) -> VersionIncrement:
        check_results = (check(current_version) for check in self.checks)
        return VersionIncrement(
            min(
                (x for x in check_results),
                key=attrgetter('value'),
                default=VersionIncrement.skip,
            )
        )

    def register(self, check: VersionEstimator):
        self.checks.append(check)


def dummy_version_estimator_skips(
    current_version: Version,
) -> VersionIncrement:
    sys.stderr.write(
        'Dummy version estimator called on version {current_version}\n'
    )
    return VersionIncrement.skip


def dummy_version_estimator_major(
    current_version: Version,
) -> VersionIncrement:
    sys.stderr.write(
        'Dummy version estimator called on version {current_version}\n'
    )
    return VersionIncrement.major
