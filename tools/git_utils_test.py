import os
import pathlib
import subprocess
import tempfile
import unittest

from tools import git_utils


class TestGitUtils(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory using a context manager
        self.test_dir = tempfile.TemporaryDirectory()

    @property
    def tmp_path(self) -> pathlib.Path:
        return pathlib.Path(self.test_dir.name)

    def tearDown(self):
        # Cleanup the temporary directory
        self.test_dir.cleanup()

    def test_git_utils(self):
        # Initialize a git repository
        subprocess.check_call(['git', 'init'], cwd=self.tmp_path)
        subprocess.check_call(['git', 'config', '--local', 'user.name', 'tester'], cwd=self.tmp_path)
        subprocess.check_call(['git', 'config', '--local', 'user.email', 'tester@testing.com'], cwd=self.tmp_path)

        # Create a test file and commit it
        test_file = self.tmp_path / 'test_file.txt'
        test_file.write_text('hello')

        subprocess.check_call(['git', 'add', 'test_file.txt'],
                              cwd=self.tmp_path)
        subprocess.check_call(['git', 'commit', '-m', 'Initial commit'],
                              cwd=self.tmp_path)

        # XXX: Insert my code
        files_tracked = git_utils.ls_files(git_directory=self.tmp_path)
        self.assertEqual(files_tracked, [
            test_file.relative_to(self.tmp_path),
        ])

if __name__ == '__main__':
    unittest.main()
