## How To

### Configure direnv

```
sudo apt-get install direnv
# Configure hook for shell (see instructions from //tools:bazel_env)
```

### Add a new Tool

- Add it to //multitool.lock.json
- `cd tools; ln -s _multitool_run_under_cwd.sh <tool>`
- You should now be able to call `./tools/<tool>`

#### To re-expose a tool to direnv

```
bazel run //tools:bazel_env
```

- will list the tools now available on PATH and update the tools if they've
  changed
- `direnv` will populate these for you when entering the directory

### Aspect CLI / AXL tasks

The `aspect` CLI is pinned in `//multitool.lock.json` and exposed on PATH the
same way as the other multitool binaries (via `bazel run //tools:bazel_env` +
direnv, or `./tools/aspect` directly).

Repo automation lives in AXL (a typed Starlark dialect):

- `//MODULE.aspect` registers tasks with `use_task(...)`.
- `//.aspect/tasks/*.axl` define them with `task(...)`.

Each registered task becomes a subcommand:

```
aspect check       # wraps ./lint.sh --mode check
aspect fmt         # wraps ./lint.sh --mode format
aspect test_all    # ctx.bazel.test over //... (accepts target patterns)
```

Add a task by writing a `task(...)` in an `.axl` file and adding a `use_task`
line to `//MODULE.aspect`. See https://docs.aspect.build/cli for the `ctx` API.

## References

- https://blog.aspect.build/run-tools-installed-by-bazel: Recommends the
  `_multitool_run_under_cwd.sh` approach, but later `bazel-devenv` updates the
  approach
- https://blog.aspect.build/bazel-devenv
- https://docs.aspect.build/cli: Aspect CLI + AXL documentation
