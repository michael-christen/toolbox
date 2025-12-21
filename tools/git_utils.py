import collections
import dataclasses
import datetime
import pathlib
import subprocess
from typing import Sequence

from tools import git_pb2


@dataclasses.dataclass
class FileCommitMap:
    """Describe how the current files map to past commits."""

    # Keyed by commit to set of files changed
    commit_map: dict[str, set[pathlib.Path]]
    # Keyed by file, to set of commits involved in
    file_map: dict[pathlib.Path, list[str]]

    def to_proto(self) -> git_pb2.FileCommitMap:
        msg = git_pb2.FileCommitMap()
        for c, files in self.commit_map.items():
            msg.commit_map[c].files.extend([str(f) for f in files])
        for f, commits in self.file_map.items():
            msg.file_map[str(f)].commits.extend(commits)
        return msg

    @classmethod
    def from_proto(cls, proto_map: git_pb2.FileCommitMap) -> "FileCommitMap":
        file_map = {}
        commit_map = {}
        for f, f_entry in proto_map.file_map.items():
            file_map[pathlib.Path(f)] = list(f_entry.commits)
        for c, c_entry in proto_map.commit_map.items():
            commit_map[c] = set(pathlib.Path(f) for f in c_entry.files)
        return cls(commit_map=commit_map, file_map=file_map)


def _get_git_output(
    args: Sequence[pathlib.Path | str], git_directory: pathlib.Path | str
) -> list[str]:
    output = subprocess.check_output(["git", "-C", git_directory] + list(args))
    result = output.decode("utf-8").strip()
    if not result:
        return []
    else:
        return result.split("\n")


def ls_files(git_directory: pathlib.Path | str) -> list[pathlib.Path]:
    """Wrapper around ls-files."""
    output = _get_git_output(["ls-files"], git_directory)
    return [pathlib.Path(p) for p in output]


def _get_args_for_after(after: datetime.datetime | None) -> list[str]:
    if after is not None:
        after_s = after.strftime("%Y-%m-%d")
        return [f'--after="{after_s}"']
    else:
        return []


# Handles renames well, but a prohibitive to run against the entire repo
# Walking the entire repo and viewing changes at each takes about 500ms with my
# current repo. Doing it with each file takes about 6 times slower at 2.87s
def list_file_commits(
    file: pathlib.Path | str,
    git_directory: pathlib.Path | str,
    after: datetime.datetime | None = None,
) -> list[str]:
    """List commits a file has touched."""
    args = (
        ["log", "--follow", "--pretty=%H"]
        + _get_args_for_after(after)
        + ["--", file]
    )
    return _get_git_output(args, git_directory)


def get_commits(
    git_directory: pathlib.Path | str,
    target: str = "HEAD",
    after: datetime.datetime | None = None,
) -> list[str]:
    args = ["rev-list", target] + _get_args_for_after(after)
    return _get_git_output(args, git_directory)


def get_files_changed_at_commit(
    commit: str, git_directory: pathlib.Path | str
) -> list[pathlib.Path]:
    """List the files changed at a commit."""
    args = ["diff-tree", "--no-commit-id", "--name-only", "-r", commit]
    return [pathlib.Path(p) for p in _get_git_output(args, git_directory)]


# Most likely want follow to preserve name
def get_file_commit_map_from_follow(
    git_directory: pathlib.Path | str,
    after: datetime.datetime | None = None,
) -> FileCommitMap:
    commit_map: dict[str, set[pathlib.Path]] = {}
    file_map: dict[pathlib.Path, list[str]] = {}
    files = ls_files(git_directory)
    commits = get_commits(git_directory=git_directory, after=after)
    # Keep ordering
    for c in commits:
        commit_map[c] = set()
    for f in files:
        f_commits = list_file_commits(
            f, git_directory=git_directory, after=after
        )
        file_map[f] = f_commits
        for c in f_commits:
            commit_map[c].add(f)
    return FileCommitMap(commit_map=commit_map, file_map=file_map)


def get_file_commit_map_from_list(
    git_directory: pathlib.Path | str,
    after: datetime.datetime | None = None,
) -> FileCommitMap:
    commit_map = {}
    file_map = collections.defaultdict(list)
    commits = get_commits(git_directory=git_directory, after=after)
    for c in commits:
        files = get_files_changed_at_commit(c, git_directory=git_directory)
        commit_map[c] = set(files)
        for f in files:
            file_map[f].append(c)
    return FileCommitMap(commit_map=commit_map, file_map=file_map)


def get_head_commit(git_directory: pathlib.Path | str, num_prev_commits: int = 0) -> str:
    result = _get_git_output(['rev-parse', f'HEAD^{num_prev_commits}'], git_directory)
    assert len(result) == 1
    return result[0]


def get_merge_base(commit_a: str, commit_b: str, git_directory: pathlib.Path | str) -> str:
    result = _get_git_output(['merge-base', commit_a, commit_b], git_directory)
    assert len(result) == 1
    return result[0]


def is_dirty(git_directory: pathlib.Path | str) -> bool:
    result = _get_git_output(['status', '--porcelain'], git_directory)
    return len(result) > 0
