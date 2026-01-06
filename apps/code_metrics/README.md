## Track Repo / Target Metrics across Commits

### Tasks

- Upload metrics for every PR and commit to main branch
  - stored as GH workflow archive
  - also uploaded to postgres database
- View
  - PR diff in-comment
  - Historical trends with something like grafana

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

#### Data Structure

- Commit:
  - revision: <commit SHA>
  - parent_revision: <commit SHA>
    - useful for comparisons

- Run:
  - created_at: timestamp
  - run_url: should be unique

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

- Database Visualizer
- Grafana
- Export to `.csv`
- Pandas scripts
- Custom web-app
- Use "intelligence" tool

##### Views

- metrics over time
- table of deltas
