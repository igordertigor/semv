import sys
import warnings
from . import errors
from . import commands


def main():
    try:
        print(commands.version_string())
    except errors.NoNewVersion:
        warnings.warn('No changes for new version')
        sys.exit(1)
    except errors.InvalidCommitType:
        sys.exit(2)
