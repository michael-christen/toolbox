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
```

Then run the tool to get the generated csv and gml

Then "analyze" and refine the results, answering the questions above

Side-quests:
- how long are different parts of this taking / what are the pain points?


## Overall Observations

|               | [drake] | [monogon] | [bzd]          | [tensorflow] | [pigweed] | [abseil]  |
| ------------- | ------- | --------- | -------------- | ------------ | --------- | --------- |
| `build //...` | 1,388 s | 1,296 s   | 1,080 s (fail) | (fail)       |           | (unknown) |
| `test //...`  | 247 s   | 192 s     | (stuck at end) |              |           | (unknown) |

## Specific Studies

### [drake]
### [monogon]
### [bzd]
### [tensorflow]
### [pigweed]
### [abseil]


[abseil]: https://github.com/abseil/abseil-cpp
[pigweed]: https://github.com/google/pigweed
[monogon]: https://github.com/monogon-dev/monogon
[bzd]: https://github.com/blaizard/bzd
[tensorflow]: https://github.com/tensorflow/tensorflow
[drake]: https://github.com/RobotLocomotion/drake
