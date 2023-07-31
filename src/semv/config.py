from typing import Dict, Any, Optional, Set
import os
import tomli
from dataclasses import dataclass, field
from .types import InvalidCommitAction


@dataclass
class Config:
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
        for key in cfg:
            if key.startswith('commit_types'):
                cfg[key] = set(cfg[key])
            elif key == 'invalid_commit_action':
                cfg[key] = InvalidCommitAction(cfg[key])
        return cls(**cfg)


def parse_toml_section(s: str) -> Dict[str, Any]:
    cfg = tomli.loads(s)
    semv_config = cfg.get('tool', {}).get('semv')
    if semv_config:
        return semv_config
    else:
        return {}
