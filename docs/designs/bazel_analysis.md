### Recap

It's now 2025-03-26, I've technically been messing around with this since
2024-11-18 or before. I've been keeping miscellaneous logs in [[log]]. I've
added several utilities to:

- parse bazel protobufs
- analyze graph attributes
- grab git log to determine likelihood of a file change
- display a bokeh/panel application with the graph
  - this ended up not quite working for a larger repo
  - to view the whole graph, there are a few tools that specialize in graphs of
    this size
    - https://github.com/gephi/gephi seems like the most promising one for data
      exploration
- figured out how to best setup jupyter notebooks for exploration within a bazel
  monorepo
- played around with pandas I ended up finding this
  [talk](https://www.youtube.com/watch?v=k4H20WxhbsA&ab_channel=GoogleOpenSource)
  ([slides](https://docs.google.com/presentation/d/1McLw_yWbPuR1UqaoowHMsu5LskPJX7kWETkB-DkqNpo/edit?resourcekey=0-sVMAbv967ww2kWvJuzyN5w#slide=id.g1867ddcecfb_0_5287))
  that does very similar things to what I'm trying to do. I took notes on it in
  [[bazelcon_2022_driving_architectural_improvements_with_dependency_metrics]].

### To Do

- [x] What's the name of that graph tool? -> https://github.com/gephi/gephi
  - https://github.com/tweag/skyscope works, but wasn't the main one
  - https://github.com/AlexTereshenkov/dg-query?tab=readme-ov-file is another
    tool for analyzing dependencies
- [ ] Perform an analysis on drake
- [ ] Show this running on a simple setup to act as a control / test case
- [ ] Decide on what questions we're answering, then design the tooling to help
      answer those questions

## Design

This bazel analysis tooling is purely a tool to aid in monitoring and improving
the dependency graph for a monorepo. There are a few stages of the development
flow where this sort of tooling could be helpful: when a change is added, this
could inform what effect is had, or when attempting to refactor this could
provide insight on where the most change could be exerted, it could also help
keep track of repo "health" over time. As an analysis tool, it's helpful to
consider what the main questions this tool helps answer.

### Main Questions the Tool Answers

#### Where would refactoring effort be most useful?

Synonyms:

- where do we have the deepest dependency chains
- what node has the highest "expected value"
- where can we take advantage of dependency inversion

#### How can we refactor a given bottleneck?

- We should help provide information that will let folks understand how to
  correct particular problems
- This could be as simple as displaying the subgraph that includes a particular
  node

#### What is the effect of a change?

Synonyms:

- how much compute does this change add to / remove from
  - this CI run
  - the average CI run
- how is the dependency graph effected

#### What is the "health" of the repository?

- how does it change over time
- how helpful could refactoring be / is it necessary

#### What does the repository look / "feel" like?

- ideally we can use this tool for exploration and uncover new questions that we
  might not think to ask
- ideally we could help identify more metrics that help inform the other
  questions or provide some level of "extensibility" for others, smarter than
  us, to develop things further

### What the Tool Should Provide

#### Simple Collection of Information

While we may ask folks to perform some of the steps to produce this information,
we should at least provide strong guidance for the production of information.
Once we have the information that we desire, our tool will collect it into a
useful format. That information likely consists of:

- Dependency Graph (via bazel query)
- Probability of Change (via git history)
- Cost of target (via test and build logs)

##### Details

- The form of the dependency graph we get is a bazel
  [`QueryResult`](https://github.com/bazelbuild/bazel/blob/f1ae4b861d496d303abc9b09edef456fd7878238/src/main/protobuf/build.proto#L500)
  - We can turn this into a networkx `DiGraph` where the label of the target is
    the node key, there is additional metadata we can parse like `node_class`,
    etc
- The probability of change can be obtained by parsing `git log` output
  - Additional complexity is added to account for file renames
  - The naive approach also assumes all target modifications are independent of
    one another, which isn't always the case
  - Caveats
    - What's a good time base to look back on and still be relevant, the entire
      time may be too large, is the past month too short?
- The duration of a target can be obtained for
  - tests: `--build_event_binary_file` outputs a delimited stream of
    [`BuildEvent`](https://github.com/bazelbuild/bazel/blob/f1ae4b861d496d303abc9b09edef456fd7878238/src/main/java/com/google/devtools/build/lib/buildeventstream/proto/build_event_stream.proto#L1413)
    this includes information on test runs, which we can use to associate a time
    with a given label
  - build timing isn't found in the `BuildEvent`, but there is an execution log
    which does contain information on each target's execution. This can be
    gathered during build by passing `--experimental_execution_log_compact_file`
    argument, this outputs a zstd compressed delimited protobuf of
    [`ExecLogEntry`](https://github.com/bazelbuild/bazel/blob/f1ae4b861d496d303abc9b09edef456fd7878238/src/main/protobuf/spawn.proto#L219),
    these can get total time for building each node, including network time,
    etc.
    - The timing is sometimes broken down further than a total time, it's a bit
      unclear which of the entries will be most helpful for our use case
  - Caveats
    - You'll likely want to be careful when running these as timing will vary
      between machines and you'll want to avoid network differences from
      impacting the results. It might be nice to normalize these a bit to
      account for machine differences, but for now, we may best think of this as
      a "relative measurement" and perhaps later try to correlate with actual
      timing of builds, etc.
    - This can also be rather expensive to capture, as you likely want to
      rebuild the entire repo at these points without caching to ensure you're
      getting accurate measurements. You may be able to use a tool like
      [`bazel-diff`](https://github.com/Tinder/bazel-diff) to limit what you
      re-run, but if you don't, I'd imagine you could either re-use past results
      or fill in unknowns with an average cost associated with the type, etc.
    - I'm not sure how we'd want to weigh the build and test time, would we want
      to simply sum them, or take one or the other?
      - When utilizing these cost metrics, I'm not too sure which will be the
        most helpful, my gut is that test time is the main factor, but that's
        probably over-stressing my use case
    - These metrics presume a single label is only built in a certain manner and
      that we don't re-build with various configs
- We should likely provide the ability to manually override certain values

###### Example Workflow

```bash
Example Script:

repo_dir=`pwd`
file_commit_pb=$repo_dir/file_commit.pb
query_pb=$repo_dir/s_result.pb
bep_pb=$repo_dir/test_all.pb
out_gml=$repo_dir/my.gml
out_csv=$repo_dir/my.csv
out_html=$repo_dir/my.html

# Prepare data
bazel query "//..." --output proto > $query_pb
bazel test //... --build_event_binary_file=$bep_pb
# Separate step if we want build timing data
bazel clean
bazel build --noremote_accept_cached \
    --experimental_execution_log_compact_file=exec_log.pb.zst \
    //...
bazel run //apps/bazel_parser -- git-capture --repo-dir \
        $repo_dir --days-ago 400 --file-commit-pb $file_commit_pb
```

###### Open Questions

- [ ] Can we turn more of this into a "single call" and remove burden from the
      user
- [ ] Should the query simply be `//...` or `deps(//...)`
  - I've noticed that tweaking the query can be helpful to limit the graph we're
    describing, but I suppose we could restrict that later
- [ ] How long should we look to the past for probability information.

#### Derivation of relevant metrics

Once we've collected the information we care about, the next step will be to use
it to compute relevant metrics for answering our questions and understanding the
repository.

We may want to provide a configuration mechanism for folks to add to this
initial set of metrics and possibly filter out some of them when viewing, etc.

###### Node Metrics

| Category        | Attribute                     | Description                                                                                                                                                                                                                                                               |
| --------------- | ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **metadata**    |                               |                                                                                                                                                                                                                                                                           |
|                 | `node_name`                   | The bazel label associated with the node                                                                                                                                                                                                                                  |
|                 | `node_class`                  | The class of the rule in the query, eg) `java_library`                                                                                                                                                                                                                    |
| **raw metrics** |                               |                                                                                                                                                                                                                                                                           |
|                 | `node_duration_s`             | A configurable combination of test and build time for the node                                                                                                                                                                                                            |
|                 | `node_probability_cache_hit`  | 1 - (# of commits this file changed)/(# of commits observed)                                                                                                                                                                                                              |
| **graph**       |                               |                                                                                                                                                                                                                                                                           |
|                 | `num_parents/children`        | Equivalent to in/out_degree                                                                                                                                                                                                                                               |
|                 | `num_ancestors/descendants`   | The total # of nodes that depend on you / you depend on                                                                                                                                                                                                                   |
|                 | `ancestor/descendant_depth`   | The max shortest path of this node to all leaves in forward and reverse.                                                                                                                                                                                                  |
|                 | `betweenness_centrality`      | The sum of the fraction of all-pairs shortest pairs that pass through the node                                                                                                                                                                                            |
|                 | `closeness_centrality`        | The reciprocal of the average shortest path                                                                                                                                                                                                                               |
|                 | `pagerank`                    |                                                                                                                                                                                                                                                                           |
|                 | `hubs/autorities_metric`      |                                                                                                                                                                                                                                                                           |
| **derived**     |                               |                                                                                                                                                                                                                                                                           |
|                 | `num_source_descendants`      | The # of nodes in the graph that can change (source files essentially) that you depend on<br> - [ ] perhaps we could remove this                                                                                                                                          |
|                 | `num_duration_ancestors`      | The # of nodes in the graph that depend on you and have a duration associated with them. This only really makes sense when test time is the only thing used for `duration`, otherwise all labels would have an associated duration<br> - [ ] perhaps we could remove this |
|                 | `ancestors_by_descendants`    | `num_ancestors` \* `num_descendants`                                                                                                                                                                                                                                      |
|                 | `group_probability_cache_hit` | Product(all descendant's node_probability_cache_hit) \* node's                                                                                                                                                                                                            |
|                 | `ancestors_by_node_p`         | `num_ancestors` \* (1 - `node_probability_cache_hit`)                                                                                                                                                                                                                     |
|                 | `ancestors_by_group_p`        | `num_ancestors` \* (1 - `group_probability_cache_hit`)<br> an unweighted version of `expected_duration_s`                                                                                                                                                                 |
|                 | `group_duration_s`            | Sum of ancestor's durations + node's                                                                                                                                                                                                                                      |
|                 | `expected_duration_s`         | `group_duration_s` \* (1 - `group_probability_cache_hit`)                                                                                                                                                                                                                 |

Note that edge direction for us means "depends on", so a child of a node is a
library that is depended upon. This is the opposite of the edge meaning in the
[[bazelcon_2022_driving_architectural_improvements_with_dependency_metrics]]
discussion.

- [ ] Consider additional metrics
  - ancestor_depth is the max shortest path for that node, we probably also want
    to use "longest path" as well ... well it's computationally tricky, so let's
    leave it alone for now

##### Repository-Wide / Node-Aggregated Metrics

| Attribute                                                           | Description                                                                                                                                                                                                                                                                                    |
| ------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `max_depth`                                                         | How deep is the overall graph                                                                                                                                                                                                                                                                  |
| `num_nodes` (order)                                                 |                                                                                                                                                                                                                                                                                                |
| `num_edges` (size)                                                  |                                                                                                                                                                                                                                                                                                |
| `density`                                                           |                                                                                                                                                                                                                                                                                                |
| `diameter`                                                          | The length of the shortest path between the 2 most distant nodes in the graph (maximum eccentricity) [`networkx`](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.distance_measures.diameter.html#networkx.algorithms.distance_measures.diameter) |
| `radius`                                                            | The minimum eccentricity [`networkx`](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.distance_measures.radius.html#networkx.algorithms.distance_measures.radius)                                                                                 |
| `num_connected_components`                                          | [`networkx.number_connected_components`](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.components.number_connected_components.html)                                                                                                             |
| `total_duration_s`                                                  |                                                                                                                                                                                                                                                                                                |
| `expected_duration_s`                                               |                                                                                                                                                                                                                                                                                                |
| `probable_nodes_affected_per_change`<br> by themselves and by group |                                                                                                                                                                                                                                                                                                |
| `max()` of most of the node attributes?                             |                                                                                                                                                                                                                                                                                                |

- [ ] If there are any particularly small connected components, maybe those
      should be filtered out / maybe we should pick the largest from each?

#### Configuration / Refinement of the data

The graphs we produce will often be very large and some refinement of the search
space will be desired to make sense of the large space, removing
clutter/artifacts of the build tree. So, we should provide some mechanism for
folks to iterate on their initial collection of information as well as to remove
sets of nodes in the graph (while preserving the structure of the graph). This
could possibly fit into the initial query stage, or possibly a refinement after
we've collected data. This will likely be an iterative/manual process that
someone goes through while configuring a repository. We'd likely want to specify
a configuration format for folks to save their specifications in as well as some
initial suggestions for how to go about refinement / generation of plots, etc
that may help show areas where refinement could be helpful.

##### Details

Most of the metrics we've been talking about don't matter much at this stage.
For refinement, we largely are just looking to exclude nodes that we don't care
about; ones that mostly just add noise. To that end, we pretty much just have
the `node_class` and the `node_name` to disambiguate. We can specify a
configuration format that'll make it easy to perform these exclusions.

To aid in this step, we can make it easy to view the distribution of
`node_class` as well as the list of nodes in node_classes and the results of our
exclusions.

- [ ] When we remove nodes, what should we do with duration and probabilities?
  - for now, we'll do nothing
- [ ] We should likely remove connected components that are below some
      threshold, may change graph metrics (density, etc)

#### Data Visualization

Let's split this into 2 sections: the common case, and the exploration case.
Visualization could be as simple as a list of targets to investigate, or as
complicated as a well-notated graph. A key part of this visualization is that
its easily interacted with: searched, filtered, grouped, etc.

##### Data Visualization for Exploration

When developing more "common mode" visualizations and path-finding we'll
selfishly want to support the free-form exploration of the data so we can figure
out what may be important, etc. In this case, we'll likely want to have produced
a table format of data where the rows are individual nodes and the columns are
the various derived metrics. Separately, we'll also likely want to expose the
graph of nodes in a way that could be easily traversed, etc.

##### Data Visualization for Answering Common Questions

As we uncover what is more and more helpful we can setup tooling to make
answering the common questions much easier. This could take the form of a
generated report, eg)

```
The top 10 bottlenecks in the dependency tree are:
- //a:b
- //b:c
- ...
```

Or, perhaps more usefully, they could likely maintain their tabular format as
the exploration section so more context is available, but the knobs are
simplified. Essentially, this could be an "optimized" version of the
"Visualization for Exploration" case.

#### Views

Most of what we've discussed so far has revolved around identifying bottleneck
nodes at a given point in time. To make things a bit more explicit, let's break
them out into a few different axes:

- scope: what are we measuring / observing:
  - single node
    - what can we understand about this node to improve how it interacts with
      the rest of the system
      - what's the subgraph it's connected to, etc.
  - all nodes (looking for node-specific metrics)
    - comparing to the rest of the nodes / "which ones should we change"
  - repository (what's the aggregated status of all nodes)
    - comparing to other repositories / a basis for "is this healthy"
- time: when are we looking
  - now: we only care about the present state of the system and how to improve
    it
  - change: we want to compare "now" to a single "baseline"
  - historical trend: we want to view how different metrics change over time
    - "change" is a special case of a trend (only 2 points of comparison)
