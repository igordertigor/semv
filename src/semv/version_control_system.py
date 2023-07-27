from typing import Iterator
import json
import subprocess
from .interface import Version, VersionControlSystem, RawCommit


class Git(VersionControlSystem):
    def get_current_version(self) -> Version:
        v = (
            subprocess.check_output('git tag', shell=True)
            .decode('utf-8')
            .splitlines()[-1]
        )

        return Version.from_string(v)

    def get_commits_without(
        self, current_version: Version
    ) -> Iterator[RawCommit]:
        fmt = {
            'sha': '%h',
            'title': '%s',
            'body': '%b',
        }
        cmd = (
            f"git log --pretty='{json.dumps(fmt)}%n' {current_version}...HEAD",
        )
        commits = subprocess.check_output(
            cmd,
            shell=True,
        ).decode('utf-8')
        for json_commit in commits.split('\n\n'):
            if len(json_commit):
                yield RawCommit(**json.loads(json_commit.replace('\n', ' ')))
