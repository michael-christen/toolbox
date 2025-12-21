"""Run metrics collection, upload, comparison, etc."""

import datetime
import json
import pathlib
import subprocess

from tools import bazel_utils
from tools import git_utils


def collect_repo_stats(workspace_dir: pathlib.Path):
    num_files = git_utils.get_num_files(workspace_dir)
    print(
        "\n".join(
            [
                f"{num_files=}",
            ]
        )
    )


def collect_target_stats(workspace_dir: pathlib.Path):
    data = bazel_utils.run_query(['attr(tags, "\\bcc_size\\b", //...)'])
    targets = []
    target_to_data = {}
    for target in data.target:
        assert target.rule.HasField("name")
        # XXX: Handle other cases?
        targets.append(target.rule.name)
        print(f"- {target.rule.name}")
        for attr in target.rule.attribute:
            if attr.name == "outs":
                target_to_data[target.rule.name] = attr.string_list_value
    # XXX: .bazelrc may not be getting picked up "--config=quiet" failed ...
    subprocess.check_call(["bazel", "build"] + targets, cwd=workspace_dir)
    bazel_bin = bazel_utils.get_bazel_bin_directory()
    for data_labels in target_to_data.values():
        for datum in data_labels:
            datum_path = bazel_bin / bazel_utils.normalize_label(datum)
            datum_val = json.loads(datum_path.read_text())
            # XXX: Collect some content
            print(datum_val)


def get_commit_information(
    now: datetime.datetime, workspace_dir: pathlib.Path, main_branch: str
):
    current_commit = git_utils.get_head_commit(
        git_directory=workspace_dir, num_prev_commits=0
    )
    parent_commit = git_utils.get_head_commit(
        git_directory=workspace_dir, num_prev_commits=1
    )
    merge_base = git_utils.get_merge_base(
        "HEAD", main_branch, git_directory=workspace_dir
    )
    current_branch = git_utils.get_branch(workspace_dir)
    is_dirty = git_utils.is_dirty(workspace_dir)
    msg = "\n".join(
        [
            f"current_commit: {current_commit}",
            f"parent_commit: {parent_commit}",
            f"merge_base: {merge_base}",
            f"current_branch: {current_branch}",
            f"is_dirty: {is_dirty}",
            f"datetime: {now}",
        ]
    )
    print(msg)


def main():
    # XXX: Pass in from CI / change default to main too
    main_branch = "master"
    now = datetime.datetime.now(datetime.timezone.utc)
    workspace_dir = bazel_utils.get_workspace_directory()
    # XXX: Maybe move "now" to run information
    get_commit_information(
        now=now, main_branch=main_branch, workspace_dir=workspace_dir
    )
    collect_target_stats(workspace_dir=workspace_dir)
    collect_repo_stats(workspace_dir=workspace_dir)


if __name__ == "__main__":
    main()
