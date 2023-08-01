from .increment import DefaultIncrementer
from .parse import AngularCommitParser
from .version_control_system import Git
from .config import Config
from . import errors
from .types import Version, VersionIncrement


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
    cp = AngularCommitParser(config.invalid_commit_action)
    vi = DefaultIncrementer(
        config.commit_types_minor,
        config.commit_types_patch,
        config.commit_types_skip,
        config.invalid_commit_action,
    )

    current_version = vcs.get_current_version()
    commits_or_none = (
        cp.parse(c) for c in vcs.get_commits_without(current_version)
    )
    commits = (c for c in commits_or_none if c is not None)
    inc = vi.get_version_increment(commits)
    if inc == VersionIncrement.skip:
        raise errors.NoNewVersion
    return current_version + inc
