"""Run metrics collection, upload, comparison, etc."""

import datetime
import json
import os
import pathlib
import subprocess

from tools import bazel_utils
from tools import git_utils


def collect_repo_stats(workspace_dir: pathlib.Path) -> None:
    num_files = git_utils.get_num_files(workspace_dir)
    print(
        "\n".join(
            [
                f"{num_files=}",
            ]
        )
    )


def collect_target_stats(workspace_dir: pathlib.Path) -> None:
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
    now: datetime.datetime,
    workspace_dir: pathlib.Path,
    head_ref: str,
    base_ref: str,
) -> None:
    current_commit = git_utils.get_head_commit(
        git_directory=workspace_dir, num_prev_commits=0
    )
    parent_commit = git_utils.get_head_commit(
        git_directory=workspace_dir, num_prev_commits=1
    )
    merge_base = git_utils.get_merge_base(
        head_ref, base_ref, git_directory=workspace_dir
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


def collect_github_stats() -> None:
    """Collect information from GITHUB Workflow.

    Reference:
    https://docs.github.com/en/actions/reference/workflows-and-actions/variables
    """
    if os.environ.get("CI") != "true":
        print("No GH info")
        return
    server_url = os.environ.get("GITHUB_SERVER_URL")
    repository = os.environ.get("GITHUB_REPOSITORY")
    run_id = os.environ.get("GITHUB_RUN_ID")
    run_attempt = os.environ.get("GITHUB_RUN_ATTEMPT")
    msg = "\n".join(
        [
            f"{server_url=}",
            f"{repository=}",
            f"{run_id=}",
            f"{run_attempt=}",
        ]
    )
    print(msg)


def main():
    # XXX: Pass in from CI / change default to main too
    base_ref = "origin/" + os.environ.get("GITHUB_BASE_REF", "master")
    # head_ref = os.environ.get("GITHUB_HEAD_REF", "HEAD")
    head_ref = "HEAD"
    print(f"{base_ref=}, {head_ref=}")
    now = datetime.datetime.now(datetime.timezone.utc)
    workspace_dir = bazel_utils.get_workspace_directory()
    # XXX: Maybe move "now" to run information
    get_commit_information(
        now=now,
        head_ref=head_ref,
        base_ref=base_ref,
        workspace_dir=workspace_dir,
    )
    collect_target_stats(workspace_dir=workspace_dir)
    collect_repo_stats(workspace_dir=workspace_dir)
    collect_github_stats()


if __name__ == "__main__":
    main()
