# Case Study: Bazel Parser

Let's try using this on several repositories to refine its behavior.

To find some representative sets, I perused github for repositories that were
active, had a large history, used bazel, and ideally were representative
monorepos. I had a tough time finding great monorepo examples, [drake] was
probably the best one I could find. Here are the 6 repos I'm using:

- [drake]
- [monogon]
- [bzd]
- [tensorflow]
- [pigweed]
- [abseil]

We'll use these as representative sets to try my tool against. For each
repository, I'd like to:

1. Identify a few possible improvements / pain points of the dependency graph
2. Get a grasp of the repository layout / architecture

During this process, I'm hoping to identify common and uncommon questions I ask
and processes I follow so that i can refine the tool to support those cases.

## Methods

For each repository

```
bazel clean
bazel build --experimental_execution_log_compact_file=exec_log.pb.zst //...
# OR
# bazel build --execution_log_compact_file=exec_log.pb.zst //...

bazel query //... --output proto > query_result.pb

bazel test //... --build_event_binary_file=test_all.pb

# From my own repository:
repo_dir=/home/mchristen/tmp/drake

bazel run --output_groups=-mypy //apps/bazel_parser:cli git-capture -- \
  --repo-dir $repo_dir --days-ago 28 --file-commit-pb $repo_dir/file_commit.pb
bazel run --output_groups=-mypy //apps/bazel_parser:cli process -- \
--query-pb $repo_dir/query_result.pb --bep-pb $repo_dir/test_all.pb \
--file-commit-pb $repo_dir/file_commit.pb --out-gml $repo_dir/my.gml --out-csv $repo_dir/my.csv
```

Then run the tool to get the generated csv and gml

Then "analyze" and refine the results, answering the questions above

Side-quests:
- how long are different parts of this taking / what are the pain points?


## Overall Observations

|               | [monogon] | [abseil]  | [bzd]          | [pigweed] | [drake] | [tensorflow] |
| ------------- | --------- | --------- | -------------- | --------- | ------- | ------------ |
| `build //...` | 1,296 s   | (unknown) | 1,080 s (fail) | 1,284 s   | 1,388 s | (fail)       |
| `test //...`  | 192 s     | (unknown) | (stuck at end) | 23 s      | 247 s   | (fail)       |
| `num_nodes`   | 1,409     | 2,488     | 2,930          | 10,800    | 27,778  | 62,271       |
| `num_edges`   | 2,123     | 4,298     | 6,779          | 21,606    | 72,683  | 292,828      |

## Specific Studies

### [drake]

A very large graph initially
![[Pasted image 20250407224526.png]]
Lots of peripheral points that are effectively disconnected
### [monogon]
This is a bit of a "wispy" graph
![[Pasted image 20250407230112.png]]
### [bzd]
SVG clusters
![[Pasted image 20250407230522.png]]
### [tensorflow]
Could only run on `//tensorflow/...` and even that took quite a long time to analyze. The different towers seem to be different histories / testdata and utilities. The right cluster is a bunch of python by the looks of it and the left cluster is more of the C++.
![[Pasted image 20250408073536.png]]
Partitioning by "Modularity Class" can be helpful
![[Pasted image 20250408074353.png]]
### [pigweed]
We got a big boy, the 2 main clusters seem to be the JS and the C++?
![[Pasted image 20250407230924.png]]
The unknown is generated .dwp and .stripped. The npm_package_store_internal is also a large contributor
### [abseil]
A fair bit smaller and more focused on C++. The bottom (egg) is timezones.
![[Pasted image 20250407225531.png]]


[abseil]: https://github.com/abseil/abseil-cpp
[pigweed]: https://github.com/google/pigweed
[monogon]: https://github.com/monogon-dev/monogon
[bzd]: https://github.com/blaizard/bzd
[tensorflow]: https://github.com/tensorflow/tensorflow
[drake]: https://github.com/RobotLocomotion/drake
