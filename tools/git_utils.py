import collections
import dataclasses
import datetime
import enum
import pathlib
import re
import subprocess
from typing import Sequence

import tqdm

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
    # XXX: ugh, testing equality with this is annoying
    # return ['584a8baf3ff9a5cda9945b1ba97a6421154ca2ac^..HEAD']
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
# XXX: This has issues with copies / sees more than it should
# XXX: Didn't find a few files too
# - b2d98b30772ec8ec9de1b0025d77ae0ce81c3088
# tensorflow/lite/g3doc/android/tutorials/text_classification.md
# tensorflow/lite/g3doc/android/tutorials/object_detection.md
# tensorflow/compiler/jit/compilability_check_util_test.cc
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
    for f in tqdm.tqdm(files):
        f_commits = list_file_commits(
            f, git_directory=git_directory, after=after
        )
        file_map[f] = f_commits
        for c in f_commits:
            commit_map[c].add(f)
    return FileCommitMap(commit_map=commit_map, file_map=file_map)


def _parse_git_logs(logs: list[str], files: list[pathlib.Path]) -> FileCommitMap:
    commit_map: dict[str, set[pathlib.Path]] = {}
    file_map: dict[pathlib.Path, list[str]] = {}
    pattern = re.compile(
        r"^(?P<type>[AMD])\s+(.+?)(\s*->\s*(.+))?$|^(?P<replace>R)(\d+)\s+(.+?)\s*->\s*(.+)$|^(?P<commit>[0-9a-f]{40})$"  # noqa
    )
    # XXX: Get the commit sha, find files affected, append to sha for file
    # XXX: Ensure in right order
    for line in logs:
        line = line.strip()
        if not line:
            continue
        match = pattern.match(line)
        if match:
            commit: str | None = match.group('commit')
            typ: str | None = match.group('type')
            replace: str | None = match.group('replace')
            if commit:
                print(f'Commit: {match.group("commit")}')
            elif typ:
                print(f'{typ=}')
            elif replace:
                print(f'{replace=}')
            if match.group(1):  # For A, M, D statuses
                change_type = match.group(1)
                old_file = match.group(2)
                # XXX: Named args
                # XXX: Doesn't make sense
                new_file = match.group(4) if match.group(4) else None
                print(f"Change type: {change_type}, Old file: {old_file}, "
                      f"New file: {new_file}")
            elif match.group(5):  # For R status (renames)
                change_type = 'R'
                similarity_index = match.group(5)
                old_file = match.group(6)
                new_file = match.group(7)
                print(f"Change type: {change_type}, Similarity index:"
                      f" {similarity_index}, Old file: {old_file}, New file:"
                      f" {new_file}")
        else:
            print(f"'{line}' did not match pattern")
    return FileCommitMap(commit_map=commit_map, file_map=file_map)


class ParseState(enum.Enum):
    PRE_COMMIT = enum.auto()
    PRE_TYPE_OR_COMMIT = enum.auto()
    PRE_SINGLE_FILE = enum.auto()
    PRE_DOUBLE_FILE = enum.auto()


class OperationType(enum.Enum):
    ADD = 'A'
    MODIFY = 'M'
    DELETE = 'D'
    REPLACE = 'R'
    TYPE_CHANGE = 'T'


def get_file_commit_map_from_log(
    git_directory: pathlib.Path | str,
    after: datetime.datetime | None = None,
) -> FileCommitMap:
    output = subprocess.check_output(
        [
            "git",
            "-C",
            git_directory,
        ] + [
            "log",
            "--name-status",
            '--pretty=format:"%H"',
            # This will format with null characters rather than spacing
            "-z",
        ]
        + _get_args_for_after(after),
        text=True,
    )
    lines = output.strip("\x00").split("\x00")

    commit_map: dict[str, set[pathlib.Path]] = {}
    file_map: dict[pathlib.Path, list[str]] = collections.defaultdict(list)
    for f in ls_files(git_directory):
        file_map[f] = []

    all_tokens = []
    for line in lines:
        all_tokens.extend(line.split('\n'))
    state = ParseState.PRE_COMMIT
    commit: str | None = None
    files: list[str] = []
    op_type: OperationType | None = None
    # Don't track a file unless it was present at HEAD
    # XXX: Maybe make this optional?
    untracked_files: set[pathlib.Path] = set()
    # track renames back to the name used at HEAD
    f_to_canonical: dict[pathlib.Path, pathlib.Path] = {}
    # XXX: Modularize this parsing
    for token in all_tokens:
        # XXX: Need to strip?
        token = token.strip()
        if not token:
            continue

        new_commit: str | None = None
        new_state: ParseState
        if len(token) == 42 and token[0] == '"' and token[-1] == '"':
            new_commit = token[1:-1]

        # Handle State Machine
        if state == ParseState.PRE_COMMIT:
            # Only looking for commit
            if new_commit is None:
                raise ValueError(
                    f"Found no commit, when that was the only option:"
                    f" '{token}'"
                )
            commit = new_commit
            commit_map[commit] = set()
            new_state = ParseState.PRE_TYPE_OR_COMMIT
        elif state == ParseState.PRE_TYPE_OR_COMMIT:
            # Could get commit or type
            if new_commit is not None:
                commit = new_commit
                commit_map[commit] = set()
                new_state = ParseState.PRE_TYPE_OR_COMMIT
            else:
                if len(token) < 1:
                    raise ValueError('Empty token when expected type')
                raw_type = token[0]
                new_op_type = OperationType(raw_type)
                if new_op_type in {OperationType.ADD, OperationType.MODIFY,
                               OperationType.DELETE, OperationType.TYPE_CHANGE}:
                    if len(token) > 1:
                        raise ValueError(f'Unexpected extra: {token}')
                    op_type = new_op_type
                    new_state = ParseState.PRE_SINGLE_FILE
                elif new_op_type == OperationType.REPLACE:
                    # Nothing to do with similarity
                    _ = int(token[1:])
                    op_type = new_op_type
                    new_state = ParseState.PRE_DOUBLE_FILE
                else:
                    raise ValueError(f'Unknown type: {new_op_type} {token}')
        elif state == ParseState.PRE_SINGLE_FILE:
            assert len(token) > 0
            assert commit is not None
            assert op_type is not None
            files.append(token)
            # This is where the magic happens
            # - update files changed in the commit
            # - update the commits for a given file
            # - handling renames and untracked files
            if op_type == OperationType.ADD:
                assert len(files) == 1
                f = pathlib.Path(files[0])
                f = f_to_canonical.get(f, f)
                if f not in untracked_files:
                    commit_map[commit].add(f)
                    file_map[f].append(commit)
                    # XXX: Should we note that we now expect to never see this
                    # again? Nope, could've gotten deleted and added back
            elif op_type in {OperationType.MODIFY, OperationType.TYPE_CHANGE}:
                # Same as add, but don't need to worry about not-tracking (if
                # we decide to do that)
                assert len(files) == 1
                f = pathlib.Path(files[0])
                f = f_to_canonical.get(f, f)
                if f not in untracked_files:
                    commit_map[commit].add(f)
                    file_map[f].append(commit)
            elif op_type == OperationType.DELETE:
                assert len(files) == 1
                f = pathlib.Path(files[0])
                # If it got deleted and re-added before
                if f not in file_map:
                    untracked_files.add(f)
                else:
                    commit_map[commit].add(f)
                    file_map[f].append(commit)
            elif op_type == OperationType.REPLACE:
                assert len(files) == 2
                old_f = pathlib.Path(files[0])
                new_f = pathlib.Path(files[1])
                new_f = f_to_canonical.get(new_f, new_f)
                f_to_canonical[old_f] = new_f
                if new_f not in untracked_files:
                    commit_map[commit].add(new_f)
                    file_map[new_f].append(commit)
            else:
                raise ValueError(f'Unknown type: {op_type} {token}')

            files.clear()
            op_type = None
            new_state = ParseState.PRE_TYPE_OR_COMMIT
        elif state == ParseState.PRE_DOUBLE_FILE:
            assert op_type == OperationType.REPLACE
            assert len(token) > 0
            files.append(token)
            new_state = ParseState.PRE_SINGLE_FILE
        else:
            raise ValueError(f'Unhandled state: {state}')
        state = new_state
    assert state in {ParseState.PRE_TYPE_OR_COMMIT, ParseState.PRE_COMMIT}
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


def get_head_commit(
    git_directory: pathlib.Path | str, num_prev_commits: int = 0
) -> str:
    result = _get_git_output(
        ["rev-parse", f"HEAD^{num_prev_commits}"], git_directory
    )
    assert len(result) == 1
    return result[0]


def get_num_files(git_directory: pathlib.Path | str) -> int:
    result = _get_git_output(["ls-files"], git_directory)
    return len(result)
