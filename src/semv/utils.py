from typing import Type
import sys
from .types import InvalidCommitAction


def warn_or_raise(message: str, action: InvalidCommitAction, etype: Type[Exception]):
    if action == InvalidCommitAction.error:
        raise etype(message)
    elif action == InvalidCommitAction.warning:
        sys.stderr.write(f'WARNING: {message}\n')
    return
