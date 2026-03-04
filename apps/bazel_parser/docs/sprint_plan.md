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

- [x] Write sprint plan ✅ 2026-03-03

### Mar 4 — Off

### Mar 5 — Correctness Fixes + Data Collection

- [x] Resolve `expected_duration_s` math ambiguity
  - Current formula (`group_duration_s * (1 - group_probability_cache_hit)`) is
    correct. Node-level and graph-level metrics answer different questions and
    are both valid. Removed XXX comment.
- [ ] Investigate `--notool_deps` question from PR #185
  - Run `bazel query` with and without the flag, compare graph sizes, decide
    whether to apply by default
- [ ] Investigate all related XXXs
- [x] Fix `follow` vs `log` discrepancy
  - `from_log` is the correct implementation (single git call, proper rename
    tracking, no known bugs). Updated `full` to use it. Removed dead
    `_parse_git_logs` function and unused `re` import. Removed
    `get_file_commit_map_from_follow` entirely. Cleaned up remaining debug
    `print` statements and stale `follow_map` references in test.
- [ ] Restore `git_utils.py` test coverage
- [ ] **Evening: kick off data collection for all repos overnight**
  - abseil, drake, pigweed, monogon, bzd (tensorflow only if feeling ambitious)
  - Run after correctness fixes so outputs are based on fixed code
  - Write `apps/bazel_parser/collect.sh`: a script that takes a repo dir and
    output dir and runs `bazel query`, `bazel test`, `git-capture`, and
    `process` to produce CSV + GML for that repo
  - Invoke it for each repo and let run overnight

### Mar 6 — Abseil Analysis

- [ ] Abseil case study (2,488 nodes — small, fast to iterate)
- [ ] Complete to acceptance criteria

### Mar 7 — Drake Analysis

- [ ] Drake case study (27,778 nodes)
- [ ] Complete to acceptance criteria

### Mar 8 — Drake Complete + Pigweed Start

- [ ] Finish drake if not complete
- [ ] Begin pigweed case study (10,800 nodes)

### Mar 9 — Pigweed + Additional Repos

- [ ] Complete pigweed case study
- [ ] If time: monogon or bzd case study

### Mar 10 — Metric Triage

- [ ] Review metric utility notes across all completed case studies
- [ ] **Metric triage**: decide:
  - Which metrics consistently surface actionable signal → Tier 1 (always
    computed)
  - Which are slow and haven't provided unique value → Tier 2 (opt-in flag)
  - Expensive candidates: `ancestor_depth`, `descendant_depth`,
    `betweenness_centrality`, `closeness_centrality` (all involve APSP or O(VE)
    passes)
- [ ] Implement `--full-metrics` flag (or equivalent) to gate tier 2 metrics

### Mar 13 — PyPI Packaging Start

- [ ] Assess proto file situation: `build_pb2.py`, `git_pb2.py`, BEP protos are
      Bazel-generated — decide whether to pre-generate and vendor or generate at
      install time
- [ ] Start `pyproject.toml` setup, entry points for CLI

### Mar 14 — PyPI Complete

- [ ] Complete packaging (proto files, dependencies, entry point)
- [ ] Publish to PyPI (even as `0.1.0-alpha` / pre-release)
- [ ] End-to-end test: fresh install from PyPI → run workflow → open in gephi
- [ ] Fix anything that breaks

### Mar 15 — Documentation

- [ ] Getting-started guide: "run these N bazel commands to collect data, then
      `pip install bazel-parser && bazel-parser process ...`"
- [ ] Fill `[ ] TODO` links in `README.md`
- [ ] Add gephi recommendation for graph visualization (replace panel as primary
      recommendation for large repos)
- [ ] Note panel app is still available for small repos

### Mar 16 — Slides Draft

- [ ] Write full slide deck in markdown
  - Suggested structure:
    1. The problem (build graph bottlenecks, hard to see at scale)
    2. How the tool works (data collection → graph → metrics)
    3. Case study findings: abseil, drake, pigweed
    4. How to run it yourself (PyPI + N bazel commands)
    5. What's next / call for contribution

### Mar 17 — Slides Polish

- [ ] Polish markdown slides
- [ ] Transition to Google Slides

### Stretch Goals

- [ ] consider reversing direction here (X depends on Y; Y is the ancestor
      instead of the descendant); would allow more standardization / make a bit
      more sense (dependencies must come before their dependent)

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
