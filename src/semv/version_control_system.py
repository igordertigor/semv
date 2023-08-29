from typing import Iterator
import json
import re
import subprocess
from .interface import Version, VersionControlSystem, RawCommit


class Git(VersionControlSystem):
    def get_current_version(self) -> Version:
        v = (
            subprocess.check_output('git tag', shell=True)
            .decode('utf-8')
            .splitlines()
        )

        if v:
            return Version.from_string(v[-1])
        else:
            return Version(major=0)

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
                yield sanitize_commit_json(json_commit)


def sanitize_commit_json(text: str) -> RawCommit:
    pattern = r'\{"sha": "(?P<sha>.*)", "title": "(?P<title>.*)", "body": "(?P<body>.*)"\}'
    m = re.search(pattern, text, re.DOTALL)
    if m:
        commit_dict = m.groupdict()
    else:
        # Fallback
        commit_dict = json.loads(text.replace('\n', ' '))
    return RawCommit(
        **{key: value.strip() for key, value in commit_dict.items()}
    )
