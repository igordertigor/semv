from .types import InvalidCommitAction

commit_types_minor = {'feat'}
commit_types_patch = {'fix', 'perf'}
commit_types_skip = {'chore', 'test', 'docs', 'ci', 'refactor', 'style'}

invalid_commit_action = InvalidCommitAction.warning
