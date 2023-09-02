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
                lines.extend(self.format_breaking_commit('', c))

        for scope, commits in breaking_commits.items():
            for c in commits:
                lines.extend(self.format_breaking_commit(scope, c))
        return '\n'.join(lines)

    def format_breaking_commit(self, scope: str, commit: Commit) -> List[str]:
        if scope:
            out = [f'- {scope}: {commit.summary}']
        else:
            out = [f'- {commit.summary}']
        for summary in commit.breaking_summaries:
            out.append(f'  - {summary}')
        return out

    def format_release_commits(
        self, types: Iterator[str], commits: GroupedCommits
    ) -> str:
        lines: List[str] = []
        for type_name in types:
            type_commits = commits.pop(type_name, None)
            if type_commits:
                lines.append(f'# {self.translate_types(type_name)}')

            if type_commits:

                general = type_commits.pop(':global:', None)
                if general:
                    lines.extend(self.format_scope('General', general))

                for scope, cmts in type_commits.items():
                    lines.extend(self.format_scope(scope, cmts))

        return '\n'.join(lines)

    def format_scope(self, scope: str, commits: List[Commit]) -> List[str]:
        if len(commits) == 1:
            return [f'- {scope}: {commits[0].summary}']
        elif len(commits) > 1:
            return [f'- {scope}:'] + [f'  - {c.summary}' for c in commits]
        else:
            return []

    def translate_types(self, name: str) -> str:
        translations = {
            'feat': 'New features',
            'feature': 'New features',
            'fix': 'Fixes',
            'perf': 'Performance Improvements',
            'performance': 'Performance Improvements',
        }
        return translations.get(name, name)
