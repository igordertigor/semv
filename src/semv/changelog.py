from typing import List, Dict, Iterator
from collections import defaultdict

from .types import Commit


GroupedCommits = Dict[str, Dict[str, List[Commit]]]


class Changelog:
    def group_commits(self, commits: Iterator[Commit]) -> GroupedCommits:

        out: GroupedCommits = defaultdict(lambda: defaultdict(list))
        for commit in commits:
            if commit.breaking:
                out['breaking'][commit.scope].append(commit)
            else:
                out[commit.type][commit.scope].append(commit)
        return out

    def format_breaking(
        self, breaking_commits: Dict[str, List[Commit]]
    ) -> str:
        lines: List[str] = []
        if breaking_commits:
            lines.append('# Breaking changes')
        general = breaking_commits.pop(':global:', None)
        if general:
            for c in general:
                lines.append(f'- {c.summary}')
                for summary in c.breaking_summaries:
                    lines.append(f'  - {summary}')
        for scope, commits in breaking_commits.items():
            for c in commits:
                lines.append(f'- {scope}: {c.summary}')
                for summary in c.breaking_summaries:
                    lines.append(f'  - {summary}')
        return '\n'.join(lines)

    def format_commits(self, types: Iterator[str], commits: GroupedCommits) -> str:
        lines: List[str] = []
        for type_name in types:
            type_commits = commits.pop(type_name, None)
            if type_commits:
                lines.append(f'# {self.translate_types(type_name)}')

            if type_commits:
                general = type_commits.pop(':global:', None)
                if general:
                    lines.extend(f'- General: {c.summary}' for c in general)
                for scope, cmts in type_commits.items():
                    if len(cmts) == 1:
                        lines.extend(f'- {c.scope}: {c.summary}' for c in cmts)
                    elif len(cmts) > 1:
                        lines.append(f'- {scope}:')
                        for c in cmts:
                            lines.append(f'  - {c.summary}')

        return '\n'.join(lines)

    def translate_types(self, name: str) -> str:
        translations = {
            'feat': 'New features',
            'feature': 'New features',
            'fix': 'Fixes',
            'perf': 'Performance Improvements',
            'performance': 'Performance Improvements',
        }
        return translations.get(name, name)
