# Sprint Plan: Bazel Analysis — Meetup Presentation (2026-03-18)

## Goal

Present the bazel analysis tooling at a Bazel meetup (~30–50 people). The talk
should demo the tool, share concrete findings from running it against real
repos, and give attendees a way to run it on their own repos afterward.

## Out of Scope (explicitly cut)

- Repo health over time / time-series tracking (allude to it as a future
  direction: "combine several snapshots")
- Notebook cleanup/consolidation (#211)
- New metrics or features beyond what case studies surface as useful
- BES backend (#165)

## Case Study Acceptance Criteria

A case study entry in `case_study.md` is complete when it contains:

- **Graph-level health metrics**: density, max depth, num nodes/edges, num
  connected components, total/expected duration
- **Top 3–5 bottleneck nodes** by the most informative metric(s), with a plain
  English explanation of why each is interesting
- **At least one concrete suggested improvement**: e.g. "splitting `//x:y` would
  reduce cache invalidations for N downstream targets"
- **1–2 gephi screenshots** illustrating the structure or a specific bottleneck
- **Metric utility notes**: which metrics surfaced useful signal for this repo,
  which didn't — feeds into the triage on Mar 12

## Day-by-Day Plan

### Mar 3 — Planning

- [x] Write sprint plan ✅ 2026-03-03 ➕ 2026-03-03 📅 2026-03-03

### Mar 4 — Off

### Mar 5 — Correctness Fixes + Data Collection

- [x] Resolve `expected_duration_s` math ambiguity ➕ 2026-03-03 📅 2026-03-05
      ✅ 2026-03-03
  - Current formula (`group_duration_s * (1 - group_probability_cache_hit)`) is
    correct. Node-level and graph-level metrics answer different questions and
    are both valid. Removed XXX comment.
- [x] Investigate `--notool_deps` question from PR #185 ➕ 2026-03-03 📅
      2026-03-05 ✅ 2026-03-04
  - `//...` returns same 376 nodes with or without flag; flag reduces edge set
    (proto size 654KB→637KB). `deps(//...)` is 46x larger — confirmed `//...` is
    correct default. `--notool_deps` removes exec-config dep edges (build tool
    mechanics); added to default query. `ignore_external=True` in parsing
    already handles `@` external labels. Removed XXX comment.
- [x] Investigate all related XXXs ➕ 2026-03-03 📅 2026-03-05 ✅ 2026-03-05
  - Removed stale/answered XXXs in cli.py, repo_graph_data.py, refinement.py,
    repo_graph_data_test.py, and git_utils.py. Converted `print(graph_metrics)`
    to `logger.info` with a TODO. Deferred ~12 XXXs that need case study data or
    are design questions for Mar 10+.
- [x] Fix `follow` vs `log` discrepancy ➕ 2026-03-03 📅 2026-03-05 ✅
      2026-03-03
  - `from_log` is the correct implementation (single git call, proper rename
    tracking, no known bugs). Updated `full` to use it. Removed dead
    `_parse_git_logs` function and unused `re` import. Removed
    `get_file_commit_map_from_follow` entirely. Cleaned up remaining debug
    `print` statements and stale `follow_map` references in test.
- [x] Restore `git_utils.py` test coverage ➕ 2026-03-03 📅 2026-03-05 ✅
      2026-03-05
- [x] **Evening: kick off data collection for all repos overnight** ➕
      2026-03-03 📅 2026-03-05 ✅ 2026-03-05
  - abseil, drake, pigweed, monogon, bzd (tensorflow only if feeling ambitious)
  - Run after correctness fixes so outputs are based on fixed code
  - Write `apps/bazel_parser/collect.sh`: a script that takes a repo dir and
    output dir and runs `bazel query`, `bazel test`, `git-capture`, and
    `process` to produce CSV + GML for that repo
  - Invoke it for each repo and let run overnight

### Mar 6 — Abseil Analysis

- [x] Abseil case study (2,608 nodes) ➕ 2026-03-03 📅 2026-03-06 ✅ 2026-03-05
- [x] Complete to acceptance criteria ➕ 2026-03-03 📅 2026-03-06 ✅ 2026-03-05

### Mar 7 — Drake Analysis & Metrics Triage & Cleanup

- [x] Review metric utility notes across all completed case studies ➕
      2026-03-03 📅 2026-03-10 ✅ 2026-03-06
- [x] **Metric triage**: keep all metrics, no `--full-metrics` flag needed ➕
      2026-03-03 📅 2026-03-10 ✅ 2026-03-06
  - Centrality metrics are useful and worth computing; consolidation opportunity
    exists (6 → 2 expensive passes) but deferred as not urgent for presentation
- [x] Revisit deferred XXXs after metric triage ➕ 2026-03-05 📅 2026-03-10 ✅
      2026-03-06

  - Serialize graph_metrics to output file (cli.py)
  - Resolve node-removal attribute handling (refinement.py)
  - SOURCE_FILE inclusion decision (parsing.py)
  - Decide whether tokens need stripping (git_utils.py:~155)
  - `ancestors_by_node_p` usefulness (repo_graph_data.py)
  - `get_node()` better checking (repo_graph_data.py)
  - Remove small weakly-connected components (repo_graph_data.py)
  - label/node_name/Node naming redundancy (repo_graph_data.py)
  - Data structure design for node info (repo_graph_data.py)
  - Better k for betweenness (repo_graph_data.py)
  - determine_main group attribution (repo_graph_data.py)
  - print vs log vs return in refinement (refinement.py)
  - Log individual exclusions (refinement.py)

- [x] Drake case study (16,987 nodes filtered) ➕ 2026-03-03 📅 2026-03-07 ✅
      2026-03-05
- [x] Complete to acceptance criteria ➕ 2026-03-03 📅 2026-03-07 ✅ 2026-03-05

### Mar 8 — Drake Complete + Pigweed Start & Pypi

- [-] Assess proto file situation: `build_pb2.py`, `git_pb2.py`, BEP protos are
  ➕ 2026-03-03 📅 2026-03-15 ❌ 2026-03-16 Bazel-generated — decide whether to
  pre-generate and vendor or generate at install time
- [-] Start `pyproject.toml` setup, entry points for CLI ➕ 2026-03-03 📅
  2026-03-15 ❌ 2026-03-16
- [-] Complete packaging (proto files, dependencies, entry point) ➕ 2026-03-03
  📅 2026-03-15 ❌ 2026-03-16
- [-] Publish to PyPI (even as `0.1.0-alpha` / pre-release) ➕ 2026-03-03 📅
  2026-03-15 ❌ 2026-03-16
- [-] End-to-end test: fresh install from PyPI → run workflow → open in gephi ➕
  2026-03-03 📅 2026-03-15 ❌ 2026-03-16
- [-] Fix anything that breaks ➕ 2026-03-03 📅 2026-03-15 ❌ 2026-03-16

- [x] Finish drake ➕ 2026-03-03 📅 2026-03-08 ✅ 2026-03-05
- [x] Begin pigweed case study (19,199 nodes) ➕ 2026-03-03 📅 2026-03-08 ✅
      2026-03-05

### Mar 9 — Pigweed + Additional Repos

- [x] Complete pigweed case study ➕ 2026-03-03 📅 2026-03-09 ✅ 2026-03-05

### Mar 10 — Documentation

### Mar 13 — Slides Draft

### Mar 14 — Slides Polish

### Mar 15 — Documentation

### Mar 16 — Slides Draft

- [ ] Ensure folks have a path to run this if they'd like ➕ 2026-03-16 📅
      2026-03-16
- [ ] If time: monogon, bzd, maybe tensorflow case study ➕ 2026-03-03 📅
      2026-03-16
- [ ] Getting-started guide: "run these N bazel commands to collect data, then
      ➕ 2026-03-03 📅 2026-03-16
      `pip install bazel-parser && bazel-parser process ...`"
- [ ] Fill `[ ] TODO` links in `README.md` ➕ 2026-03-03 📅 2026-03-16
- [ ] Add gephi recommendation for graph visualization (replace panel as primary
      ➕ 2026-03-03 📅 2026-03-16 recommendation for large repos)
- [ ] Note panel app is still available for small repos ➕ 2026-03-03 📅
      2026-03-16
- [ ] Write full slide deck in markdown ➕ 2026-03-03 📅 2026-03-16
  - Suggested structure:
    1. The problem (build graph bottlenecks, hard to see at scale)
    2. How the tool works (data collection → graph → metrics)
    3. Case study findings: abseil, drake, pigweed
    4. How to run it yourself (PyPI + N bazel commands)
    5. What's next / call for contribution

### Mar 17 — Slides Polish

- [ ] Polish markdown slides ➕ 2026-03-03 📅 2026-03-17
- [ ] Transition to Google Slides ➕ 2026-03-03 📅 2026-03-17

### Stretch Goals

- [ ] **Co-change analysis**: join `file_commit.pb` with the build graph to
      surface two signals:
  - _Same-target divergence_: files in the same library that rarely change
    together (split candidate) — scored as avg pairwise co-change among active
    files (≥ MIN_CHANGES commits in window)
  - _Cross-target convergence_: library↔library file pairs with high co-change
    score (merge candidate) — filter out lib↔test pairs which are expected
  - Prototype exists; 100% file match rate on abseil-cpp confirmed. Main open
    question is whether signal holds up at drake/pigweed scale.
  - Would add a new `--file-commit-pb` input to the `report` command.
- [ ] consider reversing direction here (X depends on Y; Y is the ancestor ➕
      2026-03-03 instead of the descendant); would allow more standardization /
      make a bit more sense (dependencies must come before their dependent)
- [ ] consider how bazel-diff creates their dependency graph instead of a full
      query ➕ 2026-03-04
  - Bazel aspect that traverses deps and emits structured data (JSON, proto,
    etc.) about each target. Advantages: you control exactly what's collected,
    can attach custom metadata, runs as part of a build rather than a separate
    query phase. Downside: requires Bazel Starlark code, tightly coupled to the
    repo's rule set.
- [ ] Consider need of cquery to handle selections in the graph ➕ 2026-03-05
- [ ] why are type hint issues not caught in py_test artifacts ➕ 2026-03-05
- [ ] remove all of the `logger.debug('a')` statements in `repo_graph_data.py`
      ➕ 2026-03-05
- [x] Establish drake refinement config filtering `_redirect_test` + `unknown`
      nodes ✅ 2026-03-05
  - Config at `~/Documents/bazel_parser_data_collection/drake/config.yaml`
  - Reduced graph from 26,716 → 16,987 nodes; Tier 1 results changed (pydrake
    binding layer, not multibody, is the real bottleneck)
  - Added `--config-file` passthrough to `collect.sh`
  - **Lesson**: always establish a config before analysis on complex repos

---

## Risks

**Case study findings are hard to time-box.** If abseil and drake don't yield
interesting findings by Mar 10, narrow scope rather than keep digging — the
graph screenshots are a fallback but not a strong demo.

**PyPI packaging with proto files may surprise you.** If this hits a wall on Mar
13, the Mar 14 block is the safety net. Hard fallback:
`pip install git+https://github.com/michael-christen/toolbox` works for the
presentation without full PyPI infrastructure.

## Distribution Approach

Split workflow — users run bazel commands themselves (they already have Bazel),
save proto outputs, then run `bazel-parser process` against them. The PyPI
package contains only the analysis tool, not Bazel itself.

Future: BCR/Bazel module (issue #204) is the "native" path but not feasible in
this window.

## Visualization Approach

Output GML (gephi) and CSV. Gephi handles large graphs well. Panel app is
de-emphasized — keep for small repos, don't demo it. Mention gephi in
getting-started docs.

## References

- PR #185 (Bazel analysis) — merged, contains open TODOs
- Issue #204 — Publish to PyPI/BCR (follow-up after presentation)
- `apps/bazel_parser/docs/design.md` — core design decisions
- `apps/bazel_parser/docs/case_study.md` — running case study notes
- BazelCon 2022 talk: Driving Architectural Improvements with Dependency Metrics
  ([video](https://www.youtube.com/watch?v=k4H20WxhbsA),
  [slides](https://docs.google.com/presentation/d/1McLw_yWbPuR1UqaoowHMsu5LskPJX7kWETkB-DkqNpo/edit))
