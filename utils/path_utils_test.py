import unittest

# Module Under Test
from utils import path_utils


class TestPathUtils(unittest.TestCase):
    def test_repo_dir(self) -> None:
        # Let's check that we can see ourselves
        self.assertTrue(
            (path_utils.REPO_DIR / "utils/path_utils_test.py").exists()
        )
