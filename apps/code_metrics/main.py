"""Run metrics collection, upload, comparison, etc."""

import dataclasses
import datetime
import json
import os
import pathlib
import subprocess

import click
import psycopg2  # noqa: F401
import sqlalchemy
import tabulate
from sqlalchemy import orm

from apps.code_metrics import models
from tools import bazel_utils
from tools import git_utils


@dataclasses.dataclass
class RunInfo:
    sha_sum: str
    parent_sha_sum: str
    branch_name: str
    run_created_at: datetime.datetime
    run_url: str


def get_run_url() -> str | None:
    """Collect information from GITHUB Workflow.

    Reference:
    https://docs.github.com/en/actions/reference/workflows-and-actions/variables
    """
    if os.environ.get("CI") != "true":
        return None
    server_url = os.environ.get("GITHUB_SERVER_URL")
    repository = os.environ.get("GITHUB_REPOSITORY")
    run_id = os.environ.get("GITHUB_RUN_ID")
    run_attempt = os.environ.get("GITHUB_RUN_ATTEMPT")
    return (
        f"{server_url}/{repository}/actions/runs/{run_id}/attempts"
        f"/{run_attempt}"
    )


def get_branch_from_github_env() -> str:
    head_ref = os.environ.get("GITHUB_HEAD_REF")
    if head_ref is not None:
        # This is the case for pull_request
        return head_ref
    ref_name = os.environ.get("GITHUB_REF_NAME")
    if ref_name is None:
        raise RuntimeError("GITHUB_REF_NAME not defined")
    return ref_name


def get_run_info(
    now: datetime.datetime,
    workspace_dir: pathlib.Path,
    head_ref: str,
    base_ref: str,
) -> RunInfo:
    # Get GIT data
    current_commit = git_utils.get_head_commit(
        git_directory=workspace_dir, num_prev_commits=0
    )
    parent_commit = git_utils.get_head_commit(
        git_directory=workspace_dir, num_prev_commits=1
    )
    # Not using yet ...
    # is_dirty = git_utils.is_dirty(workspace_dir)
    run_url = get_run_url()
    if run_url is None:
        run_url = str(now)
    return RunInfo(
        sha_sum=current_commit,
        parent_sha_sum=parent_commit,
        branch_name=head_ref,
        run_created_at=now,
        run_url=run_url,
    )


def collect_repo_stats(
    workspace_dir: pathlib.Path, run_info: RunInfo
) -> models.RepoMetrics:
    num_files = git_utils.get_num_files(workspace_dir)
    return models.RepoMetrics(
        sha_sum=run_info.sha_sum,
        parent_sha_sum=run_info.parent_sha_sum,
        branch_name=run_info.branch_name,
        run_created_at=run_info.run_created_at,
        run_url=run_info.run_url,
        # Data
        num_files=num_files,
    )


def collect_target_stats(
    workspace_dir: pathlib.Path,
    run_info: RunInfo,
) -> list[models.TargetMetrics]:
    data = bazel_utils.run_query(['attr(tags, "\\bcc_size\\b", //...)'])
    targets = []
    target_to_data = {}
    for target in data.target:
        assert target.rule.HasField("name")
        # XXX: Handle other cases?
        targets.append(target.rule.name)
        for attr in target.rule.attribute:
            if attr.name == "outs":
                target_to_data[target.rule.name] = attr.string_list_value
    # XXX: .bazelrc may not be getting picked up "--config=quiet" failed ...
    subprocess.check_call(["bazel", "build"] + targets, cwd=workspace_dir)
    bazel_bin = bazel_utils.get_bazel_bin_directory()
    stats = []
    for data_labels in target_to_data.values():
        for datum in data_labels:
            datum_path = bazel_bin / bazel_utils.normalize_label(datum)
            datum_val = json.loads(datum_path.read_text())
            # XXX: Collect some content
            # XXX: Validate ...
            stats.append(
                models.TargetMetrics(
                    sha_sum=run_info.sha_sum,
                    parent_sha_sum=run_info.parent_sha_sum,
                    branch_name=run_info.branch_name,
                    run_created_at=run_info.run_created_at,
                    run_url=run_info.run_url,
                    # Data
                    target_label=datum_val["label"],
                    text=datum_val["text"],
                    data=datum_val["data"],
                    bss=datum_val["bss"],
                    # XXX: flash, ram, max_flash, max_ram
                )
            )
    return stats


def query_parent_target_stats(
    engine: sqlalchemy.Engine, parent_sha_sum: str
) -> list[models.TargetMetrics]:
    with orm.Session(engine) as session:
        statement = sqlalchemy.select(models.TargetMetrics).where(
            models.TargetMetrics.sha_sum == parent_sha_sum
        )
        return list(session.execute(statement).scalars().all())


def query_parent_repo_stats(
    engine: sqlalchemy.Engine, parent_sha_sum: str
) -> list[models.RepoMetrics]:
    with orm.Session(engine) as session:
        statement = sqlalchemy.select(models.RepoMetrics).where(
            models.RepoMetrics.sha_sum == parent_sha_sum
        )
        return list(session.execute(statement).scalars().all())


def compare_target_stats(
    target_stats: list[models.TargetMetrics],
    parent_target_stats: list[models.TargetMetrics],
) -> list[str]:
    result = []
    if not parent_target_stats:
        parent_target_stats_dict = {}
    else:
        parent_target_stats_dict = {
            stat.target_label: stat for stat in parent_target_stats
        }
    result.append("## Target Metrics\n")
    for target_stat in target_stats:
        parent_stat = parent_target_stats_dict.get(target_stat.target_label)
        diffs: dict[str, tuple[int, int | None]]
        if parent_stat is None:
            diffs = {
                "text": (target_stat.text, None),
                "data": (target_stat.data, None),
                "bss": (target_stat.bss, None),
            }
        else:
            diffs = {
                "text": (target_stat.text, parent_stat.text),
                "data": (target_stat.data, parent_stat.data),
                "bss": (target_stat.bss, parent_stat.bss),
            }
        headers = ["metric", "before", "now", "diff"]
        table = []
        for k, v in diffs.items():
            cur_val, before_val = v
            table.append(
                (
                    k,
                    before_val,
                    cur_val,
                    (
                        str(cur_val - before_val)
                        if before_val is not None
                        else "N/A"
                    ),
                )
            )
        result.append(f"### TARGET: `{target_stat.target_label}`\n")
        result.append(tabulate.tabulate(table, headers, tablefmt="github"))
        result.append("")
    return result


def compare_repo_stats(
    repo_stat: models.RepoMetrics,
    parent_repo_stat: list[models.RepoMetrics],
) -> list[str]:
    result = []
    if parent_repo_stat:
        parent_repo_metric = parent_repo_stat[0]
        parent_num_files_str = str(parent_repo_metric.num_files)
        num_files_diff_str = str(
            repo_stat.num_files - parent_repo_metric.num_files
        )
    else:
        parent_num_files_str = "missing"
        num_files_diff_str = "N/A"
    headers = ["metric", "before", "now", "diff"]
    table = [
        (
            "num_files",
            parent_num_files_str,
            str(repo_stat.num_files),
            num_files_diff_str,
        ),
    ]
    result.append("## Repo Metrics\n")
    result.append(tabulate.tabulate(table, headers, tablefmt="github"))
    result.append("")
    return result


def get_archive_format_for_stats(
        target_stats: list[models.TargetMetrics],
        repo_stat: models.RepoMetrics) -> str:
    result_dict = {
        'target_metrics': [
            target_stat.to_dict() for target_stat in target_stats
        ],
        'repo_metrics': repo_stat.to_dict(),
    }
    return json.dumps(result_dict, indent=2)


@click.command()
@click.option("--pr_comment", type=click.Path(path_type=pathlib.Path), required=True)
@click.option("--archive", type=click.Path(path_type=pathlib.Path), required=True)
def main(pr_comment: pathlib.Path, archive: pathlib.Path) -> None:
    """Handle Code Metrics.

    - Gather RunInfo
    - Collect Target and Repo Stats
    - Store stats
      - in Github Archive for debug / backup for database outage
      - as well as database
    - Retrieve stats for parent
    - Compare stats and write comparison output for usage
    """
    now = datetime.datetime.now(datetime.timezone.utc)
    workspace_dir = bazel_utils.get_workspace_directory()

    # XXX: Pass in from CI / change default to main too
    base_ref = "origin/" + os.environ.get("GITHUB_BASE_REF", "master")
    head_ref = get_branch_from_github_env()
    # XXX: merge_base seems synonmyous with get_head_commit(num_prev_commits=1)
    # / good enough for us / otherwise what're we doing with parent?
    # print(f"{base_ref=}, {head_ref=}")
    # merge_base = git_utils.get_merge_base(
    #     head_ref, base_ref, git_directory=workspace_dir
    # )
    # print(f"{merge_base=}")
    # XXX: Maybe move "now" to run information
    run_info = get_run_info(
        now=now,
        head_ref=head_ref,
        base_ref=base_ref,
        workspace_dir=workspace_dir,
    )
    target_stats = collect_target_stats(
        workspace_dir=workspace_dir, run_info=run_info
    )
    repo_stat = collect_repo_stats(
        workspace_dir=workspace_dir, run_info=run_info
    )
    archive.write_text(get_archive_format_for_stats(
        target_stats=target_stats,
        repo_stat=repo_stat))

    # XXX: Consider separating
    # XXX: Be robust to failures? or at gh level
    engine = models.get_engine()
    if engine is None:
        print("No reporting since no DB connection could be made")
        return

    with orm.Session(engine, expire_on_commit=False) as session:
        for target_stat in target_stats:
            session.add(target_stat)
        session.add(repo_stat)
        # XXX: Should we handle the database failing here or in workflow?
        session.commit()

    parent_target_stats = query_parent_target_stats(
        engine=engine, parent_sha_sum=run_info.parent_sha_sum
    )
    parent_repo_stat = query_parent_repo_stats(
        engine=engine, parent_sha_sum=run_info.parent_sha_sum
    )
    pr_comparison_lines = []
    pr_comparison_lines.extend(compare_target_stats(
        target_stats=target_stats,
        parent_target_stats=parent_target_stats,
    ))
    pr_comparison_lines.extend(compare_repo_stats(
        repo_stat=repo_stat,
        parent_repo_stat=parent_repo_stat,
    ))
    pr_comment.write_text("\n".join(pr_comparison_lines))


if __name__ == "__main__":
    main()
