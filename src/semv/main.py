from pathlib import Path
import sys
from . import errors
from . import commands
from .config import Config


def main():
    pyproject = Path('pyproject.toml')
    if pyproject.exists():
        config = Config.parse(pyproject.read_text())
    else:
        config = Config()

    if len(sys.argv) > 1 and sys.argv[1] == '--list-types':
        print(commands.list_types(config))
        sys.exit(0)

    try:
        print(commands.version_string(config), end='')
    except errors.NoNewVersion:
        sys.stderr.write('WARNING: No changes for new version\n')
        sys.exit(1)
    except errors.SuspiciousVersionIncrement as e:
        sys.stderr.write(f'ERROR: {e.args[0]}\n')
        sys.exit(3)
    except errors.InvalidCommitType as e:
        sys.stderr.write(f'ERROR: {e.args[0]}\n')
        sys.exit(2)
    except errors.InvalidCommitFormat as e:
        sys.stderr.write(f'ERROR: {e.args[0]}\n')
        sys.exit(2)
