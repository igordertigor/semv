from typing import Dict, Any, Set, List
import tomli
from dataclasses import dataclass, field
from .types import InvalidCommitAction


@dataclass
class Config:
    commit_types_major: Set[str] = field(default_factory=set)
    commit_types_minor: Set[str] = field(default_factory=lambda: {'feat'})
    commit_types_patch: Set[str] = field(
        default_factory=lambda: {'fix', 'perf'}
    )
    commit_types_skip: Set[str] = field(
        default_factory=lambda: {
            'chore',
            'test',
            'docs',
            'ci',
            'refactor',
            'style',
        }
    )
    invalid_commit_action: InvalidCommitAction = InvalidCommitAction.warning

    @classmethod
    def parse(cls, text: str):
        cfg = parse_toml_section(text)
        if 'invalid_commit_action' in cfg:
            cfg['invalid_commit_action'] = InvalidCommitAction(
                cfg['invalid_commit_action']
            )
        if 'types' in cfg:
            types_cfg = cls._reorganize_types(cfg.pop('types'))
        else:
            types_cfg = {}

        return cls(**{**types_cfg, **cfg})

    @staticmethod
    def _reorganize_types(d: Dict[str, str]) -> Dict[str, Set[str]]:
        out: Dict[str, List[str]] = {
            'commit_types_major': [],
            'commit_types_minor': [],
            'commit_types_patch': [],
            'commit_types_skip': [],
        }
        for type, level in d.items():
            if level == 'valid':
                level = 'skip'
            out[f'commit_types_{level}'].append(type)
        return {key: set(types) for key, types in out.items()}

    def format_types(self) -> str:
        out = []

        def fmt(level: str, types: Set[str]) -> List[str]:
            t = ', '.join(sorted(list(types)))
            return [
                f'Implies {level} increment:',
                f'  {t}',
            ]

        if self.commit_types_major:
            out.extend(fmt('major', self.commit_types_major))
        if self.commit_types_minor:
            out.extend(fmt('minor', self.commit_types_minor))
        if self.commit_types_patch:
            out.extend(fmt('patch', self.commit_types_patch))
        if self.commit_types_skip:
            out.extend(fmt('skip', self.commit_types_skip))
            out[-2] = 'Other valid types:'
        return '\n'.join(out)


def parse_toml_section(s: str) -> Dict[str, Any]:
    cfg = tomli.loads(s)
    semv_config = cfg.get('tool', {}).get('semv')
    if semv_config:
        return semv_config
    else:
        return {}
