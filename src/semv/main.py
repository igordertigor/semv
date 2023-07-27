import sys
from . import errors
from . import commands


def main():
    try:
        print(commands.version_string(), end='')
    except errors.NoNewVersion:
        sys.stderr.write('WARNING: No changes for new version\n')
        sys.exit(1)
    except errors.InvalidCommitType:
        sys.exit(2)
