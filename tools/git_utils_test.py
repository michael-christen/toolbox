import os
import pathlib
import subprocess
import tempfile
import unittest

from tools import git_utils


class TestGitUtils(unittest.TestCase):
    """Test the various git utilities I have.

    Setup a temporary directory, construct git files in it, and use that to
    test against.

    - [x] ls_files
    - [x] get_files_changed_at_commit
    - [x] list_file_commits
      - [ ] after
    - [x] get_commits
      - [ ] target
      - [ ] after
    - [ ] "get a commit map"
      - [x] get_file_commit_map_from_follow
      - [x] get_file_commit_map_from_list
      - [ ] try out "after"
      - [x] show renamed files
      - [ ] possibly get a benchmark, by making a super long history
    - [ ] FileCommitMap

    NOTE: We're checking the above, feel free to test more when time is
    available.
    """

    def setUp(self):
        # Create a temporary directory using a context manager
        self.test_dir = tempfile.TemporaryDirectory()
        # Cleanup the temporary directory
        self.addCleanup(self.test_dir.cleanup)

        # Initialize a git repository
        subprocess.check_call(
            ["git", "init", "--initial-branch=main"], cwd=self.tmp_path
        )
        subprocess.check_call(
            ["git", "config", "--local", "user.name", "tester"],
            cwd=self.tmp_path,
        )
        subprocess.check_call(
            ["git", "config", "--local", "user.email", "tester@testing.com"],
            cwd=self.tmp_path,
        )

    @property
    def tmp_path(self) -> pathlib.Path:
        return pathlib.Path(self.test_dir.name)

    def _cmd(self, args: list[str | pathlib.Path]) -> str:
        return (
            subprocess.check_output(args, cwd=self.tmp_path)
            .decode("utf-8")
            .strip()
        )

    def test_git_utils(self):

        # diff-tree doesn't work on the first commit (and we accept that)
        # so let's just make an empty first commit
        self._cmd(["git", "commit", "--allow-empty", "-m", "initial"])
        first_hash = self._cmd(["git", "rev-parse", "HEAD"])

        # Create a test file and commit it
        test_file = self.tmp_path / "test_file.txt"
        test_file.write_text("hello")

        self._cmd(["git", "add", "test_file.txt"])
        self._cmd(["git", "commit", "-m", "test_file"])
        test_file_commit_hash = self._cmd(["git", "rev-parse", "HEAD"])

        files_tracked = git_utils.ls_files(git_directory=self.tmp_path)
        self.assertEqual(
            files_tracked,
            [
                test_file.relative_to(self.tmp_path),
            ],
        )
        self.assertEqual(
            git_utils.get_files_changed_at_commit(
                commit=test_file_commit_hash, git_directory=self.tmp_path
            ),
            [test_file.relative_to(self.tmp_path)],
        )

        # Check follow works as expected
        self._cmd(["git", "mv", "test_file.txt", "moved_file.txt"])
        self._cmd(["git", "commit", "-m", "moved_file"])
        mv_commit_hash = self._cmd(["git", "rev-parse", "HEAD"])

        self.assertEqual(
            git_utils.list_file_commits("moved_file.txt", self.tmp_path),
            # We're picking up its original
            [mv_commit_hash, test_file_commit_hash],
        )

        self.assertEqual(
            git_utils.get_commits(self.tmp_path),
            [mv_commit_hash, test_file_commit_hash, first_hash],
        )

        # Show follow map is behaving as expected
        follow_map = git_utils.get_file_commit_map_from_follow(self.tmp_path)
        expected_follow = git_utils.FileCommitMap(
            commit_map={
                first_hash: set(),
                test_file_commit_hash: set([pathlib.Path("moved_file.txt")]),
                mv_commit_hash: set([pathlib.Path("moved_file.txt")]),
            },
            file_map={
                pathlib.Path("moved_file.txt"): [
                    mv_commit_hash,
                    test_file_commit_hash,
                ],
            },
        )
        self.assertEqual(follow_map, expected_follow)

        # Show how list misses out on tracking a file through history
        list_map = git_utils.get_file_commit_map_from_list(self.tmp_path)
        expected_list = git_utils.FileCommitMap(
            commit_map={
                first_hash: set(),
                test_file_commit_hash: set([pathlib.Path("test_file.txt")]),
                mv_commit_hash: set(
                    [
                        pathlib.Path("test_file.txt"),
                        pathlib.Path("moved_file.txt"),
                    ]
                ),
            },
            file_map={
                pathlib.Path("test_file.txt"): [
                    mv_commit_hash,
                    test_file_commit_hash,
                ],
                pathlib.Path("moved_file.txt"): [
                    mv_commit_hash,
                ],
            },
        )
        self.assertEqual(list_map, expected_list)


if __name__ == "__main__":
    unittest.main()
