from pathlib import Path
import sys
from .increment import DefaultIncrementer
from .parse import AngularCommitParser
from .version_control_system import Git
from .config import Config
from . import errors
from .types import Version, VersionIncrement


def version_string() -> Version:
    """Generate a version string for the next version

    Exceptions:
        NoNewVersion
        InvalidCommitType
    """
    pyproject = Path('pyproject.toml')
    if pyproject.exists():
        config = Config.parse(pyproject.read_text())
    else:
        config = Config()

    if len(sys.argv) > 1 and sys.argv[1] == '--list-types':
        print(config.format_types())
        sys.exit(0)

    vcs = Git()
    cp = AngularCommitParser(config.invalid_commit_action)
    vi = DefaultIncrementer(
        config.commit_types_minor,
        config.commit_types_patch,
        config.commit_types_skip,
        config.invalid_commit_action,
    )

    try:
        current_version = vcs.get_current_version()
        commits_or_none = (
            cp.parse(c) for c in vcs.get_commits_without(current_version)
        )
        commits = (c for c in commits_or_none if c is not None)
        inc = vi.get_version_increment(commits)
        if inc == VersionIncrement.skip:
            raise errors.NoNewVersion
        return current_version + inc
    except errors.InvalidCommitType as e:
        sys.stderr.write(f'ERROR: {e.args[0]}\n')
        sys.exit(2)
    except errors.InvalidCommitFormat as e:
        sys.stderr.write(f'ERROR: {e.args[0]}\n')
        sys.exit(2)
