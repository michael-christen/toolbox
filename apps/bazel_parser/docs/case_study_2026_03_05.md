# Case Study: First-Pass Analysis — March 5th 2026

Analysis of three open-source Bazel repos using the bazel-parser tool.
Data collected 2026-03-05 with a 400-day git history window.

Repos:
- [abseil-cpp](https://github.com/abseil/abseil-cpp) — C++ utility library
- [drake](https://github.com/RobotLocomotion/drake) — robotics / mathematical modeling
- [pigweed](https://github.com/google/pigweed) — embedded firmware framework

## Graph Health Summary

| Metric | abseil-cpp | drake | pigweed |
|---|---|---|---|
| Total nodes | 2,608 | 16,987 * | 19,199 |
| Source files | 1,473 | 5,198 | 5,319 |
| Tests (timed) | 245 | 8,291 | 782 |
| Graph depth (max) | 13 | 17 | 21 |
| Total test duration | 316.8s | 3,285.9s | 266.9s |
| **Expected cost/commit** | **153.3s** | **503.1s** | **12.5s** |
| **Avg nodes invalidated/commit** | **423** | **1,533** | **666** |

\* Drake filtered: 7,104 `_redirect_test` (auto-generated lint wrappers)
and 2,625 `unknown` (`.dwp`/`.stripped` artifacts) removed via
`refinement.class_patterns`. Raw query returns 26,716 nodes.

Expected cost/commit and avg nodes invalidated/commit are the headline
health metrics — they capture the combined effect of graph structure,
test duration, and historical churn rates. Pigweed's 12.5s vs. drake's
503s, despite having comparable numbers of source files, tells the
structural story better than any single metric.

---

## abseil-cpp

### Graph character

Well-structured, C++-only, 13 levels deep. The `//absl/base` cluster
is a near-universal dependency: `//absl/base:config`, `config.h`,
`options.h`, and `policy_checks.h` each have 1,100+ nodes that
transitively depend on them — nearly half the graph — covering the
full 316s test suite. Any change to these files is a whole-repo event.

### Top split candidates (Tier 1)

`//absl/synchronization:synchronization` is the single most expensive
library to change (90.6s expected, score 118k). It has 461 dependents
and 256 transitive dependencies — it aggregates broadly from both
directions. `//absl/strings:strings` (75s, 786 ancestors) is the
graph's structural lynchpin: it has the highest betweenness centrality,
meaning more dependency chains pass through it than any other library.
The `//absl/strings:cord*` cluster (cord, cordz_info, cordz_update_scope)
scores similarly and represents a natural sub-cluster that could be
isolated.

### Hot source files (Tier 2)

`config.h` leads with a change cost of 28.0 (expected rebuild-seconds
triggered per commit that touches it). `//absl/hash:internal/hash.h`
(24.8) and `//absl/container:internal/raw_hash_set.h` (21.2) are
notable: these are *internal* implementation headers, not public API,
yet they carry enormous blast radius. `raw_hash_set.h` in particular
has a low 85.4% cache-hit rate — it changes frequently *and* triggers
65s of downstream tests.

### Expensive tests (Tier 3)

`hash_test` (15.1s, 28% cache hit, 10.8s expected) and
`simulated_clock_test` (21.0s, 51% cache hit, 10.4s expected) lead.
The `random` subsystem tests (`poisson_distribution_test`,
`beta_distribution_test`, `randen_benchmarks`) cluster in the top 10
— the random library has 226 transitive dependencies, pulling in much
of the repo and invalidating these tests frequently.

### Metric utility notes

- `ancestors_by_descendants` (Tier 1 score): strong signal, surfaces
  the right libraries
- `ancestors_by_group_p` (Tier 2 score): clean signal for source files;
  the combo of change frequency × blast radius is more useful than
  either alone
- `expected_duration_s` (Tier 3): useful but benchmarks inflate results
  (`randen_benchmarks` at 23.6s raw duration); consider filtering
  `_benchmark` targets
- `betweenness_centrality`: confirmed useful (identified `strings` as
  bridge), but largely corroborates Tier 1 rather than adding new nodes

---

## drake

### Graph character

After filtering noise nodes, 16,987 nodes (down from 26,716 raw). The
7,104 `_redirect_test` nodes — auto-generated lint wrapper targets, each
fully isolated with zero edges — inflated the count by 42% without
contributing structural signal. Additionally, 2,625 `unknown` nodes
(`.dwp` DWARF package files and `.stripped` binary artifacts from build
rules) had no analytical value. Filtering these is now the recommended
first step for drake analysis.

Extremely diverse rule taxonomy (50+ node classes) reflecting heavy
bespoke build infrastructure. Graph depth of 17, 38 weakly connected
components. Expected cost/commit **503s** — nearly 8.5 minutes of test
time expected on every commit. Avg nodes invalidated per commit is 1,533,
roughly 9% of the filtered graph.

### Top split candidates (Tier 1)

After filtering, the entire top 10 is `//bindings/pydrake/*` — low-level
pybind wrappers that form the base of the Python binding layer.
`//tools/install/libdrake:drake_shared_library` leads at score 2.3M
(636 ancestors, 3,659 descendants, 330s expected duration). The
`//bindings/pydrake/common:wrap_pybind`, `cpp_param_pybind`,
`cpp_template_pybind` cluster follows tightly (scores 2.1–2.2M). These
all have nearly identical expected durations (~330s) because they share
the same massive downstream test coverage. Splitting any of these would
require restructuring the Python binding architecture.

The unfiltered run (no config) surfaced `//multibody/plant` and
`//multibody/tree` as the top Tier 1 targets because the `unknown`
artifact nodes were present as descendants of multibody targets, inflating
their `ancestors_x_descendants` scores. Post-filter, multibody remains
important but the pydrake binding layer is the structural bottleneck.

### Hot source files (Tier 2)

`//multibody/plant:multibody_plant.h` leads at change cost 36.1 (was
56.2 before filtering, due to fewer total ancestors now counted). The
`//common` headers (`drake_assert.h` at 22.2, `fmt.h` at 15.9) remain
the near-universal dependency equivalents. `//common/ad:internal/partials.cc`
and `standard_operations.cc` (12.7 each, 638s downstream) highlight the
automatic differentiation internals as high-exposure implementation files.

### Expensive tests (Tier 3)

The tutorials tests dominate: `configuring_rendering_lighting_test`
(66s, **8.3% cache hit**, 60.5s expected) and
`hydroelastic_contact_basics_test` (21.2s, 8.3% cache hit, 19.5s
expected). The ~8% cache hit rate across the tutorials cluster means
these tests re-run on nearly every commit. They depend on the pydrake
binding layer and `multibody`, so any change in either triggers them.
`//:py/install_test` (25.5s, 7.6% cache hit, 23.6s) is also notable:
an install-validation test that runs on almost every commit.

### Key lesson: always filter before analysis

The unfiltered graph's Tier 1 was misleading — `//multibody` appeared as
the top bottleneck partly because `unknown` artifact nodes attached to it
inflated its descendant count. After filtering, the actual architectural
bottleneck (pydrake binding layer) becomes clear. Establishing a
`config.yaml` with appropriate `class_patterns` is a prerequisite to
meaningful analysis for complex repos.

### Metric utility notes

- Tier 1 score magnitudes (2M+ vs. abseil's 118k) communicate severity
  well; the pydrake binding cluster is the real bottleneck
- `pagerank` produced false positives (lint tools rank above domain
  libraries); less useful than `num_ancestors` for actionable findings
- Tier 3 correctly surfaces the tutorials cluster as the highest-ROI
  CI optimization target
- The filtering step changed Tier 1 results significantly; always
  establish a config before drawing conclusions

---

## pigweed

### Graph character

19,199 nodes with an extremely diverse rule taxonomy (150+ distinct node
classes) reflecting the embedded platform abstraction architecture.
Deepest graph of the three at 21 levels. Despite this depth, the
expected cost/commit is only **12.5s** — the lowest by a large margin.
This demonstrates that depth alone is not a problem; well-isolated
layers with narrow interfaces keep the blast radius small.

The large node count is partially inflated by `npm_package_store_internal`
(3,660 nodes) and `filegroup` (1,535) — the JS/web toolchain and
platform data files contribute significantly to node count without
representing C++ build complexity.

### Top split candidates (Tier 1)

`//pw_log:pw_log` (3,954 ancestors, score 494k) and
`//pw_string:builder` (5,396 ancestors — the most of any cc_library —
score 464k) top the list. However, their expected durations are 1.2s
and 1.2s respectively. The `ancestors_x_descendants` score is high
because of enormous fan-in, but the test suite is so lean that structural
coupling doesn't translate to meaningful CI cost. The split-candidate
signal requires context from Tier 3 to be actionable here.

The exception is `//pw_bluetooth_sapphire/host/l2cap:l2cap` (830
ancestors, 581 descendants, score 482k) — the Bluetooth subsystem
stands out as structurally denser than the rest of pigweed, consistent
with it being a large protocol stack with many interdependencies.

### Hot source files (Tier 2)

`//pw_allocator:public/pw_allocator/shared_ptr.h` leads at 14.3 change
cost with 26.6s downstream tests. The `pw_allocator` cluster
(`shared_ptr.h`, `deallocator.h`, `allocator.h`) appears prominently —
this library is under active development, evident from the lower cache
hit rates. `//pw_multibuf/v2:public/pw_multibuf/v2/multibuf.h` (12.9)
is notable: a v2 API header with 98.9% cache hit that nonetheless
scores high, implying substantial downstream coverage.

### Expensive tests (Tier 3)

The expected costs are low across the board (max 0.7s), confirming the
graph is well-managed. The bluetooth proxy tests
(`pw_bluetooth_proxy_*_mbv1/v2_test`) cluster at 59-60% cache hit —
the most volatile in the repo, consistent with active bluetooth
development. `//pw_console/py:window_manager_test` (13.0s raw, 96.3%
cache hit, 0.5s expected) is the slowest test but well-cached.

### Metric utility notes

- The gap between Tier 1 scores and Tier 3 expected durations is the
  key insight: high `ancestors_x_descendants` alone doesn't indicate a
  problem when `expected_duration_s` is near zero. A normalized
  `expected_duration_fraction` (expected_duration / total_duration)
  would help comparisons across repos.
- Pigweed is the best counter-example to "depth = bad": 21 levels,
  well-factored interfaces, 12.5s expected CI cost. Useful for the
  presentation to show what good looks like.
- The bluetooth cluster consistently surfaces in all three tiers as
  the one outlier subsystem, validating the tool's ability to identify
  problem areas within an otherwise healthy repo.

---

## Cross-Repo Observations

### Expected cost/commit as the headline health metric

The ratio of expected cost/commit to total test duration:

| Repo | Expected/commit | Total tests | Ratio |
|---|---|---|---|
| abseil-cpp | 153.3s | 316.8s | 48% |
| drake (filtered) | 503.1s | 3,285.9s | 15% |
| pigweed | 12.5s | 266.9s | 5% |

Pigweed is remarkably efficient: only 5% of total test capacity is
consumed per commit on average. Abseil's 48% is high — nearly half
the test suite is effectively re-run on every commit, driven by the
`//absl/base` universal dependency cluster. Drake's 15% looks moderate
but 503s in absolute terms is the real concern.

### The universal dependency pattern

Every repo has one: `//absl/base:config` (abseil), `//common:fmt.h`
(drake), `//pw_preprocessor:pw_preprocessor` (pigweed). These are the
files/libraries that nearly everything depends on. They are typically
stable (high cache hit rate), which keeps the damage manageable, but
they represent the floor of what's achievable with caching alone. Any
regression in their change rate would immediately amplify CI cost
repo-wide.

### Depth is not the problem; coupling is

Pigweed has the deepest graph (21 levels) but the lowest CI cost.
Drake has the shallowest-ish structure but the highest cost. Graph
depth is a poor proxy for build health. The metrics that matter are
`expected_duration_s` (absolute cost) and `ancestors_x_descendants`
(structural coupling), not raw depth.

### Tier 1 vs. Tier 3 divergence as a health signal

In abseil and drake, Tier 1 and Tier 3 largely agree on which subsystems
are problematic. In pigweed, Tier 1 surfaces high-scoring libraries
but Tier 3 shows near-zero costs — the structural coupling exists but
hasn't become a CI burden yet. This divergence is itself a useful
signal: pigweed's `pw_log`/`pw_string` are candidates to monitor as
the repo grows, even if they're not actionable today.
