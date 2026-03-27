- [talk](https://www.youtube.com/watch?v=k4H20WxhbsA&ab_channel=GoogleOpenSource)
- [slides](https://docs.google.com/presentation/d/1McLw_yWbPuR1UqaoowHMsu5LskPJX7kWETkB-DkqNpo/edit?resourcekey=0-sVMAbv967ww2kWvJuzyN5w#slide=id.g1867ddcecfb_0_5287)

### Raw Notes

- opposite directionality (should pick one)
- longest dependency chain starting from A
  > At spotify we have used the maximum and average depth over the full graph as
  > measure of the flatness of the graph and to capture the improvements of
  > isolation.
- “Rebuilds targets” score as the product of changes to A and the total number
  of transitive downstreams.
  - This can be interpreted as a score for how much changes to a single target,
    affects others in the graph due to cache invalidations.
  - A high score means that you are a top cache invalidator in the graph. E.g.
    “ios_pill” that we saw in the beginning.
- we also consider the upstream depth to describe the shape of this subgraph.
- Thus we collect all changes to this targets and use this to define a score for
  “Rebuild Targets by Transitive Dependencies”.
- This is the product between the sum of all file changes affecting the
  transitive upstreams, multiplied by the total transitive downstreams
- This can be interpreted as a score for bottleneck-ness, and captures how a
  single target act as a force multiplier of graph invalidations in the graph.
- This is an improved way to identify bottlenecks that could benefit from
  isolation and cutting off the dependencies between the upstream and downstream
  side.

- Related to this metric, an important centrality measure from the research
  field of graph structures is “Betweenness centrality”.
- This is the fraction of all dependency chains between other targets that
  passes through a single build target like A.
- This can be seen as a score for the broker-ness in the dependency network and
  that could also benefit from isolation.
- https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.centrality.betweenness_centrality.html

- dependency inversion, if a single implementation is ever used, does that cause
  issues?

bazel query \
 --keep_going \
 --noimplicit_deps \
 --output xml "deps(//...)"

[spotify slides](https://docs.google.com/presentation/d/1McLw_yWbPuR1UqaoowHMsu5LskPJX7kWETkB-DkqNpo/edit?pli=1&resourcekey=0-sVMAbv967ww2kWvJuzyN5w#slide=id.g1867ddcecfb_0_5527)

- [x] List metrics
  - upstream & downstream
    - dependency depth
    - transitive targets -> num_ancestors/descendants
  - in & out (same as upstream & downstream from what I can tell)
    - degree
    - eccentricity
      - XXX: not doing this, unclear what it is
        > The eccentricity of a node v is the maximum distance from v to all
        > other nodes in G. XXX: How is this different than depth?
        # - [ ] eccentricity
        > - F this, I have no idea, let's just do depth ...
  - rebuilt targets
  - rebuilt targets by transitive dependency
  - 28d changes (node_probability_cache_hit)
  - 28d changes transitive dependency (group_probability_cache_hit)
  - (centrality)
    - betweenness
    - betweenness (longest)
      - what's this? Not implementing
        > XXX: betweennes_longest doesn't quite make sense
    - closeness
  - (link analysis)
    - pagerank
    - hub
    - authority
- [x] list views
  - graph metrics:
    - top list (histogram), click selects and shows timeline of metric as well
      as isolates the value along the distribution
      - colored by 'client'
    - select:
      - which metric to use
      - when we're evaluating
      - search target; tribe,squad,client
      - test filters: exclude, show, isolated
    - all metrics for targets selected
      - value for selected targets
      - average for ALL
      - distribution, color coded by client
  - dependency depth distribution:
    - x axis is depth (positive integers)
    - y axis is percentage
    - top view is current (separated by "client")
    - bottom view is changes over time
    - similar selection (just no metric)
    - want to move depth to the left and the graph wider
  - overall avg/pct trend
    - select metric client, exclude tests
    - x axis = time
    - series: avg, p25,50,75,90
  - overall sum trend
  - dependency depth top list
  - max dependency depth trend
  - dependency depth distribution
  - PRs that touch one system
    - not quite sure?
  - Avg systems touched per PR
  - metric definitions
- [x] try out their query and use rule_input / rule_output
  - much more data, unclear if helpful or not
- [x] try out their git approach of `git log --name-only --since 28 days ago`
  - much quicker
- [ ] support condensation
  - remove a node and anneal the edges
- [ ] describe metrics
- [ ] try more of their visualizations or equivalent

- To make it easier to understand and calculate the metrics, we have a
  condensation step Allow the developer to spec what targets to keep and which
  ones to remove. As we remove targets, we rewire the edges, keeping the same
  connective properties of the graph, and propagating decoration data forward.
- they used rebuilt targets by transitive dependency a lot
- establishing an arbitrary cap was helpful
- query -> construct -> decorate -> condense -> compute

  - bazel query
  - build graph from query
  - decorate graph with git contributions
  - collapse / condense graph with configuration
  - compute graph metrics

- [ ] what would this look like to incorporate a time series
- [ ] how to hook up to PR
