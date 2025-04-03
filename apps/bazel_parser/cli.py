r"""Parse bazel query outputs

A larger system description:
- inputs:
  - bazel query //... --output proto > query_result.pb
    - the full dependency tree
  - bazel test //... --build_event_binary_file=test_all.pb
    - bazel run //utils:bep_reader < test_all.pb
    - the execution time related to each test target
  - git_utils.get_file_commit_map_from_follow
    - how files have changed over time, can be used to generate
      probabilities of files changing in the future
- intermediates:
  - representation for source files and bazel together
- outputs:
  - test targets:
    - likelihood of executing
      - expected value of runtime
  - source files:
    - cost in execution time of modification
    - expected cost of file change (based on probability of change * cost)
  - graph with the values above, we could take any set of file inputs and
    describe cost
  - graph that we could identify overly depended upon things

XXX:
 - bazel query --keep_going --noimplicit_deps --output proto "deps(//...)"
   is much bigger than "//..." alone, compare what the differences are
- git log --since="10 years ago" --name-only --pretty=format: | sort \
        | uniq -c | sort -nr
  - this is much faster
  - could identify renames via:
    - git log --since="1 month ago" --name-status --pretty=format: \
            | grep -P 'R[0-9]*\t' | awk '{print $2, "->", $3}'
    - then correct
    - can get commit association via
      - git log --since="1 month ago" --name-status --pretty=format:"%H"
    - statuses are A,M,D,R\d\d\d
```
# Regex pattern to match the git log output
pattern = r"^([AMD])\s+(.+?)(\s*->\s*(.+))?$|^R(\d+)\s+(.+?)\s*->\s*(.+)$"
# Parse each line using the regex
for line in git_log_output.strip().split('\n'):
    match = re.match(pattern, line.strip())
    if match:
        if match.group(1):  # For A, M, D statuses
            change_type = match.group(1)
            old_file = match.group(2)
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
```

Example Script:

repo_dir=`pwd`
file_commit_pb=$repo_dir/file_commit.pb
query_pb=$repo_dir/s_result.pb
bep_pb=$repo_dir/test_all.pb
out_gml=$repo_dir/my.gml
out_csv=$repo_dir/my.csv
out_html=$repo_dir/my.html

# Prepare data
bazel query "//... - //docs/... - //third_party/bazel/..." --output proto \
        > $query_pb
bazel test //... --build_event_binary_file=$bep_pb
bazel run //apps/bazel_parser --output_groups=-mypy -- git-capture --repo-dir \
        $repo_dir --days-ago 400 --file-commit-pb $file_commit_pb
# Separate step if we want build timing data
bazel clean
bazel build --noremote_accept_cached \
    --experimental_execution_log_compact_file=exec_log.pb.zst \
    --generate_json_trace_profile --profile=example_profile_new.json \
    //...
# Would then need to process the exec_log.pb.zst file to get timing from it and
# then add to the other timing information

# Process and visualize the data
bazel run //apps/bazel_parser --output_groups=-mypy -- process \
        --file-commit-pb $file_commit_pb --query-pb $query_pb --bep-pb \
        $bep_pb --out-gml $out_gml --out-csv $out_csv
bazel run //apps/bazel_parser --output_groups=-mypy -- visualize \
        --gml $out_gml --out-html $out_html
"""

import datetime
import logging
import pathlib
import subprocess
import sys
import tempfile
import time

import click
import networkx
import pydantic
import tqdm
import yaml

from apps.bazel_parser import panel
from apps.bazel_parser import parsing
from apps.bazel_parser import refinement
from tools import bazel_utils
from tools import git_pb2
from tools import git_utils
from utils import bep_reader

logger = logging.getLogger(__name__)

PATH_TYPE = click.Path(exists=True, path_type=pathlib.Path)
OUT_PATH_TYPE = click.Path(exists=False, path_type=pathlib.Path)


class Config(pydantic.BaseModel):
    # Error if extra arguments
    model_config = pydantic.ConfigDict(extra='forbid')

    query_target: str
    test_target: str
    days_ago: int
    refinement: refinement.RefinementConfig


def load_config(config_yaml_path: pathlib.Path, overrides: dict) -> Config:
    with open(config_yaml_path, 'r') as f:
        raw_data = yaml.safe_load(f)
    # Apply overrides
    raw_data.update(overrides)
    # Validates and parses
    return Config(**raw_data)


@click.group()
def cli():
    pass


@click.command()
@click.option("--repo-dir", type=PATH_TYPE, required=True)
@click.option("--days-ago", type=int, required=True)
@click.option("--file-commit-pb", type=OUT_PATH_TYPE, required=True)
def git_capture(
    repo_dir: pathlib.Path,
    days_ago: int,
    file_commit_pb: pathlib.Path,
) -> None:
    git_query_after = datetime.datetime.now() - datetime.timedelta(
        days=days_ago
    )
    file_commit_map = git_utils.get_file_commit_map_from_follow(
        git_directory=repo_dir, after=git_query_after
    )
    file_commit_pb.write_bytes(
        file_commit_map.to_proto().SerializeToString(deterministic=True)
    )


@click.command()
@click.option("--query-pb", type=PATH_TYPE, required=True)
@click.option("--bep-pb", type=PATH_TYPE, required=True)
@click.option("--file-commit-pb", type=PATH_TYPE, required=True)
@click.option("--out-gml", type=OUT_PATH_TYPE, required=True)
@click.option("--out-csv", type=OUT_PATH_TYPE, required=True)
def process(
    query_pb: pathlib.Path,
    bep_pb: pathlib.Path,
    file_commit_pb: pathlib.Path,
    out_gml: pathlib.Path,
    out_csv: pathlib.Path,
) -> None:
    query_result = bazel_utils.parse_build_output(query_pb.read_bytes())
    with bep_pb.open("rb") as bep_buf:
        label_to_runtime = bep_reader.get_label_to_runtime(bep_buf)
    file_commit_proto = git_pb2.FileCommitMap()
    file_commit_proto.ParseFromString(file_commit_pb.read_bytes())
    file_commit_map = git_utils.FileCommitMap.from_proto(file_commit_proto)
    r = parsing.get_repo_graph_data(
        query_result=query_result,
        label_to_runtime=label_to_runtime,
        file_commit_map=file_commit_map,
    )
    graph_metrics = r.get_graph_metrics()
    # XXX: What to do with graph_metrics?
    print(graph_metrics)
    r.to_csv(out_csv)
    r.to_gml(out_gml)


@click.command()
@click.option("--repo-dir", type=PATH_TYPE, required=True)
@click.option("--days-ago", type=int, required=False)
@click.option("--config-file", type=PATH_TYPE, required=False)
@click.option("--out-gml", type=OUT_PATH_TYPE, required=False)
@click.option("--out-csv", type=OUT_PATH_TYPE, required=False)
def full(
    repo_dir: pathlib.Path,
    days_ago: int | None,
    config_file: pathlib.Path | None,
    out_gml: pathlib.Path | None,
    out_csv: pathlib.Path | None,
) -> None:
    if config_file:
        overrides = {}
        if days_ago is not None:
            overrides["days_ago"] = days_ago
        config = load_config(config_file, overrides=overrides)
    else:
        assert days_ago is not None
        config = Config(
            query_target="//...",
            test_target="//...",
            days_ago=days_ago,
            refinement=refinement.RefinementConfig(
                name_patterns = [],
                class_patterns = [],
                class_pattern_to_name_patterns = {},
            ),
        )
    # XXX: Show progress?

    # Query for graph
    logger.info('Querying...')
    query_pb = subprocess.check_output(
        ["bazel", "query", "--output", "proto", config.query_target],
        cwd=repo_dir)
    query_result = bazel_utils.parse_build_output(query_pb)
    # Test for timing
    logger.info('Testing...')
    with tempfile.NamedTemporaryFile() as tmpfile:
        bep_pb = tmpfile.name
        subprocess.check_call(
            ["bazel", "test", f"--build_event_binary_file={bep_pb}",
             config.test_target],
            cwd=repo_dir)
        with open(bep_pb, "rb") as bep_buf:
            label_to_runtime = bep_reader.get_label_to_runtime(bep_buf)
    # XXX: Optional build timing data ...
    # Capture git information
    logger.info('History from git...')
    git_query_after = datetime.datetime.now() - datetime.timedelta(
        days=config.days_ago
    )
    file_commit_map = git_utils.get_file_commit_map_from_follow(
        git_directory=repo_dir, after=git_query_after
    )
    logger.info('Parsing...')
    r = parsing.get_repo_graph_data(
        query_result=query_result,
        label_to_runtime=label_to_runtime,
        file_commit_map=file_commit_map,
    )
    logger.info('Refining...')
    refinement.full_refinement(
        repo=r,
        refinement=config.refinement,
        verbosity=refinement.Verbosity.COUNT,
    )
    logger.info('Outputting...')
    graph_metrics = r.get_graph_metrics()
    print(graph_metrics)
    if out_csv is not None:
        r.to_csv(out_csv)
    if out_gml is not None:
        r.to_gml(out_gml)
    logger.info('Done...')
    # # XXX: Run it all here!
    # cmd = ['bazel', 'test', '//...']
    # with tqdm.tqdm(desc="Query", unit="") as pbar:
    #     # XXX: stderr
    #     proc = subprocess.Popen(
    #         cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
    #         cwd=repo_dir,
    #     )
    #     while proc.poll() is None:
    #         pbar.set_postfix(status="Running")
    #         time.sleep(0.1)
    #     # XXX: probably show whilst
    #     stdout, stderr = proc.communicate()
    #     # print(stdout)
    #     pbar.set_postfix(status="Done")
    #     if proc.returncode != 0:
    #         print(stdout)
    #         print(stderr)
    #         raise RuntimeError("Failed to run command")


@click.command()
@click.option("--gml", type=PATH_TYPE, required=True)
@click.option("--out-html", type=OUT_PATH_TYPE, required=False)
def visualize(
    gml: pathlib.Path,
    out_html: pathlib.Path | None,
) -> None:
    graph = networkx.read_gml(gml)
    panel.run_panel(graph=graph, html_out=out_html)


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stderr,
                        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S",
                        level=logging.DEBUG)
    cli.add_command(git_capture)
    cli.add_command(process)
    cli.add_command(visualize)
    cli.add_command(full)
    cli()
