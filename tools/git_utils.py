import collections
import dataclasses
import datetime
import pathlib
import subprocess


def _get_git_output(args: list[pathlib.Path | str],
                    git_directory: pathlib.Path | str) -> list[str]:
    output = subprocess.check_output(['git', '-C', git_directory] + args)
    result = output.decode('utf-8').strip()
    if not result:
        return []
    else:
        return result.split('\n')


def ls_files(git_directory: pathlib.Path | str) -> list[pathlib.Path]:
    """Wrapper around ls-files."""
    output = _get_git_output(['ls-files'], git_directory)
    return [pathlib.Path(p) for p in output]


def _get_args_for_after(after: datetime.datetime | None) -> list[str]:
    if after is not None:
        after_s = after.strftime('%Y-%m-%d')
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
    args = [
            'log', '--follow', '--pretty=%H'
    ] + _get_args_for_after(after) + [
        '--', file
    ]
    return _get_git_output(args, git_directory)


def get_commits(
        git_directory: pathlib.Path | str,
        after: datetime.datetime | None = None,
        ) -> list[str]:
    args = ['rev-list', 'HEAD'] + _get_args_for_after(after)
    return _get_git_output(args, git_directory)


def get_files_changed_at_commit(commit: str,
                                git_directory: pathlib.Path | str
                                ) -> list[pathlib.Path]:
    """List the files changed at a commit."""
    args = [
        'diff-tree',
        '--no-commit-id',
        '--name-only',
        '-r',
        commit
    ]
    return [pathlib.Path(p) for p in _get_git_output(args, git_directory)]


@dataclasses.dataclass
class FileCommitMap:
    """Describe how the current files map to past commits."""

    # XXX: Do I need a dataclass if I have a single type?
    commit_map: dict[str, set[pathlib.Path]]


# XXX: maybe we want to experiment with both mechanisms?
def get_file_commit_map_from_follow(
        git_directory: pathlib.Path | str,
        after: datetime.datetime | None = None,
) -> FileCommitMap:
    commit_map = {}
    # XXX: Maybe remove?
    file_map = {}
    files = ls_files(git_directory)
    commits = get_commits(git_directory=git_directory, after=after)
    # Keep ordering
    for c in commits:
        commit_map[c] = set()
    for f in files:
        f_commits = list_file_commits(
            f, git_directory=git_directory, after=after)
        file_map[f] = f_commits
        for c in f_commits:
            commit_map[c].add(f)
    return FileCommitMap(commit_map=commit_map)


def get_file_commit_map_from_list(
        git_directory: pathlib.Path | str,
        after: datetime.datetime | None = None,
) -> FileCommitMap:
    commit_map = {}
    # XXX: Maybe remove?
    file_map = collections.defaultdict(list)
    commits = get_commits(git_directory=git_directory, after=after)
    for c in commits:
        files = get_files_changed_at_commit(c, git_directory=git_directory)
        commit_map[c] = set(files)
        for f in files:
            file_map[f].append(c)
    return FileCommitMap(commit_map=commit_map)
