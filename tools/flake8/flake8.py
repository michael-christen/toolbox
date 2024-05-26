import sys

from flake8.main import cli

from tools import utils

if __name__ == "__main__":
    utils.update_argv_with_workspace()
    sys.exit(cli.main())
