from .increment import DefaultIncrementer
from .parse import AngularCommitParser
from .version_control_system import Git
from . import config
from .types import Version


def version_string() -> Version:
    """Generate a version string for the next version

    Exceptions:
        NoNewVersion
        InvalidCommitType
    """
    vcs = Git()
    cp = AngularCommitParser()
    vi = DefaultIncrementer(config.invalid_commit_action)

    current_version = vcs.get_current_version()
    commits = (cp.parse(c) for c in vcs.get_commits_without(current_version))
    return current_version + vi.get_version_increment(commits)
