import datetime
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

    # XXX
    def xtest_parse_git_logs(self):
        example_logs = """
4f11bee540bfcde503b5bfd97e4d5e6b6748fa2d
M       README.md
M       WORKSPACE
R100    tools/csv-to-sheets/.gitignore  apps/csv-to-sheets/.gitignore
R100    tools/csv-to-sheets/csv2sheets.py       apps/csv-to-sheets/csv2sheets.py
R100    tools/csv-to-sheets/requirements.txt    apps/csv-to-sheets/requirements.txt
R100    tools/ical/README.md    apps/ical/README.md
R100    tools/ical/read_ical_rrules.py  apps/ical/read_ical_rrules.py
R100    tools/ical/requirements.txt     apps/ical/requirements.txt
M       cargo-bazel-lock.json
R100    tools/useful_commands.md        docs/useful_commands.md
R100    experiments/rust/hello-rust/.gitignore  examples/basic/.gitignore
R053    experiments/proto/hello/BUILD   examples/basic/BUILD
R100    experiments/rust/hello-rust/Cargo.lock  examples/basic/Cargo.lock
R100    experiments/rust/hello-rust/Cargo.toml  examples/basic/Cargo.toml
R100    experiments/rust/README.md      examples/basic/README.md
R072    experiments/cpp/hello/main/BUILD        examples/basic/app/BUILD
R063    experiments/cpp/hello/main/hello-greet.cc       examples/basic/app/hello-greet.cc
R100    experiments/cpp/hello/main/hello-greet.h        examples/basic/app/hello-greet.h
R067    experiments/cpp/hello/main/hello-world.cc       examples/basic/app/hello-world.cc
R100    experiments/proto/hello/hello.proto     examples/basic/hello.proto
R076    experiments/proto/hello/hello_test.py   examples/basic/hello_test.py
R070    experiments/cpp/hello/lib/BUILD examples/basic/lib/BUILD
R076    experiments/cpp/hello/lib/hello-time.cc examples/basic/lib/hello-time.cc
R100    experiments/cpp/hello/lib/hello-time.h  examples/basic/lib/hello-time.h
R100    experiments/proto/hello/main.py examples/basic/main.py
R100    experiments/rust/hello-rust/src/main.rs examples/basic/src/main.rs
D       experiments/rust/hello-rust/BUILD
A       mchristen/parsing_scripts/BUILD
R100    tools/one-offs/pocket_export_html_to_csv.py     mchristen/parsing_scripts/pocket_export_html_to_csv.py
R100    tools/one-offs/youtube_playlist_to_csv.py       mchristen/parsing_scripts/youtube_playlist_to_csv.py
D       tools/miscellaneous/convert_movies.py
D       tools/miscellaneous/trello_ex.py
D       tools/motd/README.md
D       tools/motd/config.ini
D       tools/motd/header
D       tools/motd/main.py

6b93bf84597df4ceacab7877980122196adf68cb
A       .bazelrc
M       README.md
M       WORKSPACE
M       experiments/proto/hello/BUILD
A       experiments/proto/hello/main.py

9183bcdcebe2969acfe3fca7a15897e6b9a81773
M       tools/csv-to-sheets/requirements.txt

b55ed643b81812b36517f20a682279a7c3d150e2
M       tools/csv-to-sheets/requirements.txt

1d467d8d5695b953143f3eae50628f11e8cdc236
M       tools/csv-to-sheets/requirements.txt

ba0cd16e24fc910502d1bcde83bc98f27af58c4d
M       tools/csv-to-sheets/requirements.txt

8b6fdd662c80decdfc0db993711534b07661c702
M       tools/csv-to-sheets/requirements.txt

3e98b8d2e15f3f46502a957bc191bb26e22adfe0
M       tools/csv-to-sheets/requirements.txt

ebfecbe1c8460ef7b67bae6932009374167460a9
M       tools/csv-to-sheets/requirements.txt

f29c3acaa4f95d2572426540680cb3ecec5c4f2d
M       tools/csv-to-sheets/requirements.txt

b16030608b2dc68371fb89e8e7f1e88e6d2ab3b6
159a96197ce027829412c0e6c2e4f1a6724954c3
A       .github/workflows/build-and-test.yml
M       .gitignore
A       BUILD
A       Cargo.lock
M       README.md
M       WORKSPACE
A       cargo-bazel-lock.json
A       experiments/cpp/hello/lib/BUILD
A       experiments/cpp/hello/lib/hello-time.cc
A       experiments/cpp/hello/lib/hello-time.h
M       experiments/cpp/hello/main/BUILD
M       experiments/cpp/hello/main/hello-world.cc
A       experiments/proto/hello/BUILD
A       experiments/proto/hello/hello.proto
A       experiments/proto/hello/hello_test.py
A       experiments/rust/hello-rust/BUILD
        """  # noqa
        # XXX: Maybe we have FileCommitMap just not show an entry for files
        # with empty lists? Probably not, if we want it to denote source file
        files = []
        logs = example_logs.strip().splitlines()
        output = git_utils._parse_git_logs(logs=logs, files=files)
        print(output)
        self.fail('hi')

    # XXX: Test deleted, then added back
    # XXX: Show difference in copy?
    # XXX: Type change
    # XXX: Delete, but was in f_to_canonical and added back
    def test_git_utils(self):

        # diff-tree doesn't work on the first commit (and we accept that)
        # so let's just make an empty first commit
        self._cmd(["git", "commit", "--allow-empty", "-m", "initial"])
        first_hash = self._cmd(["git", "rev-parse", "HEAD"])
        self.assertEqual(git_utils.get_num_files(self.tmp_path), 0)

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
        self.assertEqual(git_utils.get_num_files(self.tmp_path), 1)
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
            git_utils.get_head_commit(self.tmp_path, num_prev_commits=0),
            mv_commit_hash,
        )
        self.assertEqual(
            git_utils.get_head_commit(self.tmp_path, num_prev_commits=1),
            test_file_commit_hash,
        )
        self.assertEqual(git_utils.get_num_files(self.tmp_path), 1)

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
        log_map = git_utils.get_file_commit_map_from_log(self.tmp_path)
        print(log_map)  # XXX
        print(expected_follow)  # XXX
        self.assertEqual(log_map, expected_follow)

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

        # Check the proto is invertible w/ no data loss
        proto = follow_map.to_proto()
        inverted_proto = git_utils.FileCommitMap.from_proto(proto)
        self.assertEqual(follow_map, inverted_proto)

    def test_extras(self) -> None:
        self.assertEqual([], git_utils._get_args_for_after(None))
        self.assertEqual(
            ['--after="2025-01-01"'],
            git_utils._get_args_for_after(
                datetime.datetime(year=2025, month=1, day=1)
            ),
        )
