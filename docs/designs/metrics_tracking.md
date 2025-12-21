## Spike to Track Repo / Target Metrics across Commits


### Resources

- https://interrupt.memfault.com/blog/code-size-deltas
- https://pigweed.dev/pw_bloat/

### Topics

#### Calculating Deltas

- need to track "parent" since the commit before is not necessarily the parent

Find parent:

```bash
git rev-parse <commit>^1
```

> One thing to also be aware of is that if we want our code size deltas between
> commits and pull request builds to always work, we need to ensure that every
> single commit in the master branch that a developer could branch from has its
> code size calculated and stored.

Find common ancestor:

```bash
git merge-base HEAD master
```

#### Data Structure

- Commit:
    - revision: <commit SHA>
    - parent_revision: <commit SHA>
    - build: ? (perhaps it's the target?)

- Run:
    - > A unique collection within a commit
    - > could have several runs on a single commit
    - ? what data do we want?
    - created_at: timestamp
    - message: ?

- Tables per commit
    - Code Size:
        - Commit (ref)
        - target / build: what're we referencing
            - ? does this need its own table?
        - <data>
            - text
            - data
            - bss

#### Storage Type

- Options
    - CI
    - Sheets
    - git notes
    - DB

- Desires
    - likely want the ability to quickly list or export all the historical code
      sizes, query for a single build (for pull-request deltas), and be able to
      ensure that no duplicates exist.

#### Visualization

##### Options
- Export to `.csv`
- Pandas scripts
- Custom web-app
- Use "intelligence" tool
- Grafana
- Database Visualizer

##### Views

- metrics over time
- table of deltas
