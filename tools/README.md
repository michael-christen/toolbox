
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


## References
- https://blog.aspect.build/run-tools-installed-by-bazel: Recommends the
  `_multitool_run_under_cwd.sh` approach, but later `bazel-devenv` updates the
  approach
- https://blog.aspect.build/bazel-devenv
