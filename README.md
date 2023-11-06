# toolbox

My personal monorepo.

This will include everything from one-off scripts and experiments to libraries
and applications. I'll likely mostly use Python, C++, and Rust (fingers
crossed) and tie it all into 1 build tool to bring them all together.

This should act as a repository of projects I'm working on and an example of my
latest insights into best practices, design principles, dev-ops usage, etc.

## Layout

- tools: directory of various tools
- experiments: miscellaneous experiments I'm trying out

## To Do

- gitignore
- pyright, etc.
- gh tools
- handle security issues & re-enable dependabot:
  https://github.com/michael-christen/toolbox/security/dependabot
- hermetic tools
- github workflow
- using gazelle?
- dotconfig
- ssh agent and commit signing
- configure caching
- show it all
  - protobuf
  - python
  - rust
  - nanopb
  - embedded
  - javascript
  - fast api
  - django
- how to include third party code, etc.
- code format: clang-format, yapf, etc.
- XXX checks
- build install with docker, puppet, ansible or something
- testing
- serialization in general
- libraries
  - bit manipulation
- projects
  - embedded
    - C++
    - Rust
    - RTOS build
  - tools
    - stats tracking
- github squash strategy
- decide on rough rules for directory structure, likely don't separate by
  language

### Personal
- switch to ubuntu
- get tmux copy/paste working
- tmux use previous directory
- vim settings
  - std::cout "no member named 'cout' in namespace 'std'"
- bazel completion
- personal jira

## Notes

Bazel:
- use via bazelisk, keeps up to date
- [cpp](https://bazel.build/start/cpp)
  - put in experiments/cpp/hello

## Installation Instructions

```
wget -O ~/tools/bazel https://github.com/bazelbuild/bazelisk/releases/download/v1.18.0/bazelisk-linux-amd64
chmod +x ~/tools/bazel
~/tools/bazel
# Add to path
```

## Cross-referenced
- how to reproducibly install bazelisk, download and use
