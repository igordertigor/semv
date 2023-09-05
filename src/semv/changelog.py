from typing import List, Dict, Iterator, Set
from collections import defaultdict

from dataclasses import dataclass, field

from .config import Config
from .types import Commit


GroupedCommits = Dict[str, Dict[str, List[Commit]]]


@dataclass
class BreakingChange:
    scope: str
    message: str
    info: List[str]

    def __str__(self) -> str:
        lines: List[str] = []
        if self.scope == 'general':
            lines.append(f'- {self.message}')
        else:
            lines.append(f'- {self.scope}: {self.message}')
        for m in self.info:
            lines.append(f'  - {m}')
        return '\n'.join(lines)


@dataclass
class ChangelogScope:
    scope: str
    messages: List[str]

    def __str__(self) -> str:
        lines: List[str] = []
        if len(self.messages) == 1:
            (msg,) = self.messages
            if self.scope == 'general':
                lines.append(f'- General: {msg}')
            else:
                lines.append(f'- {self.scope}: {msg}')
        else:
            lines.append(f'- {self.scope}:')
            for msg in self.messages:
                lines.append(f'  - {msg}')
        return '\n'.join(lines)


@dataclass
class ChangelogData:
    breaking_changes: List[BreakingChange] = field(default_factory=list)
    major_changes: Dict[str, List[ChangelogScope]] = field(
        default_factory=dict
    )
    minor_changes: Dict[str, List[ChangelogScope]] = field(
        default_factory=dict
    )
    patch_changes: Dict[str, List[ChangelogScope]] = field(
        default_factory=dict
    )

    def __str__(self) -> str:
        segments: List[str] = []
        if self.breaking_changes:
            segments.append('# Breaking changes')
            segments.extend([str(bc) for bc in self.breaking_changes])
            segments.append('')

        for changes in [
            self.major_changes,
            self.minor_changes,
            self.patch_changes,
        ]:
            for type_name, scope_changes in changes.items():
                if scope_changes:
                    segments.append(f'# {_translate_types(type_name)}')
                    segments.extend(str(ch) for ch in scope_changes)
                    segments.append('')

        if segments and segments[-1] == '':
            segments = segments[:-1]

        return '\n'.join(segments)


class ChangelogAssembler:
    def __init__(
        self,
        commit_types_major: Set[str],
        commit_types_minor: Set[str],
        commit_types_patch: Set[str],
    ):
        self.commit_types = {
            'major': commit_types_major,
            'minor': commit_types_minor,
            'patch': commit_types_patch,
        }

    def assemble(self, commits: Iterator[Commit]) -> ChangelogData:
        out = ChangelogData()
        grouped_commits = self.group_commits(commits)
        breaking = grouped_commits.pop('breaking', None)
        if breaking:
            out.breaking_changes = self.assemble_breaking(breaking)

        for name, types in self.commit_types.items():
            setattr(
                out,
                f'{name}_changes',
                self.assemble_release_commits(iter(types), grouped_commits),
            )
        return out

    def group_commits(self, commits: Iterator[Commit]) -> GroupedCommits:

        out: GroupedCommits = defaultdict(lambda: defaultdict(list))
        for commit in commits:
            if commit.breaking:
                out['breaking'][commit.scope].append(commit)
            else:
                out[commit.type][commit.scope].append(commit)
        return out

    def assemble_breaking(
        self, breaking_commits: Dict[str, List[Commit]]
    ) -> List[BreakingChange]:
        out: List[BreakingChange] = []
        general = breaking_commits.pop(':global:', None)
        if general:
            for c in general:
                out.append(self.assemble_breaking_commit('general', c))

        for scope, commits in breaking_commits.items():
            for c in commits:
                out.append(self.assemble_breaking_commit(c.scope, c))

        return out

    def assemble_breaking_commit(
        self, scope: str, commit: Commit
    ) -> BreakingChange:
        return BreakingChange(
            scope=scope, message=commit.summary, info=commit.breaking_summaries
        )

    def assemble_release_commits(
        self, types: Iterator[str], commits: GroupedCommits
    ) -> Dict[str, List[ChangelogScope]]:
        out: Dict[str, List[ChangelogScope]] = {}
        for type_name in types:
            type_commits = commits.pop(type_name, None)
            if type_commits is None:
                continue

            out[type_name] = []

            general = type_commits.pop(':global:', None)
            if general:
                out[type_name].append(self.assemble_scope('general', general))

            for scope, cmts in type_commits.items():
                out[type_name].append(self.assemble_scope(scope, cmts))
        return out

    def assemble_scope(
        self, scope: str, commits: List[Commit]
    ) -> ChangelogScope:
        return ChangelogScope(
            scope=scope, messages=[c.summary for c in commits]
        )


def _translate_types(name: str) -> str:
    translations = {
        'feat': 'New features',
        'feature': 'New features',
        'fix': 'Fixes',
        'perf': 'Performance Improvements',
        'performance': 'Performance Improvements',
    }
    return translations.get(name, name)
