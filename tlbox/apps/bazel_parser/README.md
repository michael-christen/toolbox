# Bazel Parser

## Why?

Are your CI times longer than you think they should be? Is that caused by cache
invalidation of your build graph? This tool is meant to make it easier to
understand and improve your build graph so that you can identify key areas to
make improvements.

### Example

There are several types of issues that your repo could have, but here's one.
Let's say we have libraries: A, B, C, D, E; those depend on a utility X; X is
really just a container/wrapper for these other libraries: F, G, H, I, J. Now,
any time any of X + F-J are modified all of A-E are now invalidated. That may
not be ideal, perhaps A actually just uses a small subset of the functionality
exposed by X, maybe that could be segmented off and we could reduce how often we
require A and its friends to be rebuilt.

This sort of thing is easy to spot with a small graph, but for a large
repository it will become much more difficult. Folks who are in the trenches
likely have good intuition for areas of improvement, but it's mostly vibes based
and it's fairly difficult to support a refactor or motivate a co-worker to
change their implementation to support your valid yet vibe-based assessment.

That's where this tool comes in, it collects, combines, and refines cold hard
data and exposes it in a useful and extensible way so that you can gain deeper
insights into your repository.

## Getting Started

- [ ] Define how to get the executable

Get the executable and run the `full` command, specifying where your repository
is `--repo-dir` and what output you'd like to collect: `--out-csv` describes the
path for a csv where each node in your build graph has a row of several derived
metrics; the `--out-gml` defines a `.gml` file that encodes the connections of
the build graph as well as all of the various attributes that are also present
in the csv.

```
./bazel_parser full --repo-dir=`pwd` --out-csv=my_repo.csv --out-gml=my_gml.csv
```

You can now use your favorite spreadsheet application to play with the csv and
find interesting nodes of interest. You can load the gml as a networkx graph;
you can also use any miscellaneous graph viewer, I've had interesting
experiences with https://gephi.org/, it handles large graphs very well.

## Where to go from here?

- [ ] Link Design doc
- [ ] Link Tutorial/examples doc
- [ ] Link How To/Usage doc
- [ ] Link Reference doc
- [ ] Link Roadmap, contributions, development docs
  - We've got to provide good definitions for each field
