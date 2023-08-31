from .increment import DefaultIncrementer
from .parse import AngularCommitParser
from .version_control_system import Git
from .config import Config
from . import errors
from .types import Version, VersionIncrement, RawCommit, InvalidCommitAction
from . import hooks


def list_types(config: Config) -> str:
    return config.format_types()


def version_string(config: Config) -> Version:
    """Generate a version string for the next version

    Exceptions:
        NoNewVersion
        InvalidCommitType
        InvalidCommitFormat
        SuspiciousVersionIncrement
    """
    vcs = Git()
    cp = AngularCommitParser(
        config.invalid_commit_action,
        config.skip_commit_patterns,
    )
    vi = DefaultIncrementer(
        config.commit_types_minor,
        config.commit_types_patch,
        config.commit_types_skip,
        config.invalid_commit_action,
    )
    h = hooks.Hooks()
    for name in config.checks:
        h.register(getattr(hooks, name)(**config.checks[name]))

    current_version = vcs.get_current_version()
    commits_or_none = (
        cp.parse(c) for c in vcs.get_commits_without(current_version)
    )
    commits = (c for c in commits_or_none if c is not None)
    inc = vi.get_version_increment(commits)
    estimated_inc = h.estimate_version_increment(current_version)
    if estimated_inc.value < inc.value:
        raise errors.SuspiciousVersionIncrement(
            f'Commits suggest {inc.value} increment,'
            f' but checks imply {estimated_inc.value} increment'
        )
    if inc == VersionIncrement.skip:
        raise errors.NoNewVersion
    return current_version + inc


def commit_msg(filename: str, config: Config):
    """Check a single commit message"""
    with open(filename, 'r') as f:
        msg = f.read()
    commit_parser = AngularCommitParser(
        InvalidCommitAction.error, config.skip_commit_patterns
    )
    version_incrementer = DefaultIncrementer(
        config.commit_types_minor,
        config.commit_types_patch,
        config.commit_types_skip,
        InvalidCommitAction.error,
    )
    parsed_commit = commit_parser.parse(
        RawCommit(sha='', title=msg.strip(), body='')
    )
    if parsed_commit is not None:
        version_incrementer.get_version_increment(iter([parsed_commit]))
