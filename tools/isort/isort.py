from isort.main import main

from tools import utils

if __name__ == "__main__":
    utils.update_argv_with_workspace()
    main()
