from typing import Iterator
import json
import subprocess
from .interface import Version, VersionControlSystem, RawCommit


class Git(VersionControlSystem):
    def get_current_version(self) -> Version:
        v = (
            subprocess.check_output('git tag', shell=True)
            .decode('utf-8')
        )
        print(v)

        return Version.from_string(v)

    def get_commits_without(self, current_version: Version) -> Iterator[RawCommit]:
        fmt = {
            'sha': '%h',
            'title': '%s',
            'body': '%b',
        }
        commits = (
            subprocess.check_output(
                f"git log --pretty='{json.dumps(fmt)}' {current_version}...HEAD",
                shell=True,
            )
            .decode('utf-8')
            .splitlines()
        )
        for json_commit in commits:
            print(json_commit)
            yield RawCommit(**json.loads(json_commit))
