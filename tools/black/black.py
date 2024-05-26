import re
import sys

from black import patched_main

from tools import utils

if __name__ == "__main__":
    utils.update_argv_with_workspace()
    sys.argv[0] = re.sub(r"(-script\.pyw|\.exe)?$", "", sys.argv[0])
    sys.exit(patched_main())
