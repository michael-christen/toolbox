import collections
import collections.abc

setattr(collections, "MutableMapping", collections.abc.MutableMapping)

import os  # noqa: E402
import re  # noqa: E402
import sys  # noqa: E402

from notebook import notebookapp  # noqa: E402

if __name__ == "__main__":
    if "BUILD_WORKSPACE_DIRECTORY" in os.environ:
        os.chdir(os.environ["BUILD_WORKSPACE_DIRECTORY"])
    sys.argv[0] = re.sub(r"(-script\.pyw?|\.exe)?$", "", sys.argv[0])
    # XXX: Failing to start well
    sys.exit(notebookapp.main())
