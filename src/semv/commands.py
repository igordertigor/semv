from .increment import DefaultIncrementer
from .parse import AngularCommitParser
from .version_control_system import Git
from . import config
from . import errors
from .types import Version, VersionIncrement


def version_string() -> Version:
    """Generate a version string for the next version

    Exceptions:
        NoNewVersion
        InvalidCommitType
    """
    vcs = Git()
    cp = AngularCommitParser(config.invalid_commit_action)
    vi = DefaultIncrementer(config.invalid_commit_action)

    current_version = vcs.get_current_version()
    commits_or_none = (cp.parse(c) for c in vcs.get_commits_without(current_version))
    commits = (c for c in commits_or_none if c is not None)
    inc = vi.get_version_increment(commits)
    if inc == VersionIncrement.skip:
        raise errors.NoNewVersion
    return current_version + inc
