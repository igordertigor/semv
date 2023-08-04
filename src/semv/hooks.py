from typing import List, Union
from abc import ABC, abstractmethod
import sys
import os
import shutil
import glob
import subprocess
import tomli
from tempfile import TemporaryDirectory
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


class RunPreviousVersionsTestsTox(VersionEstimator):
    toxenv: List[str]

    def __init__(self, toxenv: Union[str, List[str]]):
        if isinstance(toxenv, str):
            self.toxenv = [toxenv]
        else:
            self.toxenv = toxenv

    def run(self, current_version: Version) -> VersionIncrement:
        source_dir = os.path.abspath(os.path.curdir)
        build_proc = subprocess.run(
            'python -m build',
            shell=True,
            capture_output=True,
        )
        build_proc.check_returncode()
        package = os.path.join(source_dir, max(glob.glob('dist/*.whl')))
        with TemporaryDirectory() as tempdir:
            git_proc = subprocess.run(
                f'git clone --depth 1 --branch {current_version}'
                f' file://{source_dir}/.git .',
                shell=True,
                capture_output=True,
                cwd=tempdir,
            )
            git_proc.check_returncode()

            possible_misleading_imports = glob.glob(
                os.path.join(tempdir, f'{get_package_name()}.*')
            )
            if possible_misleading_imports:
                src_layout = os.path.join(tempdir, 'src')
                os.makedirs(src_layout, exist_ok=True)
                for fake_import in possible_misleading_imports:
                    shutil.move(fake_import, src_layout)

            envs = ','.join(self.toxenv)
            test_proc = subprocess.run(
                f'tox --installpkg {package} -e "{envs}" -- -v',
                shell=True,
                cwd=tempdir,
                capture_output=True,
            )
            if test_proc.returncode:
                sys.stderr.write(test_proc.stdout.decode('utf-8'))
                return VersionIncrement.major
        return VersionIncrement.skip


def get_package_name() -> str:
    if os.path.exists('pyproject.toml'):
        with open('pyproject.toml') as f:
            cfg = tomli.loads(f.read())
        return cfg['project']['name']
    else:
        raise NotImplementedError(
            'Only supporting files configured through pyproject.toml at the moment'
        )
