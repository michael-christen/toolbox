# Database Management

## Overview

It's been awhile since I've interacted with databases, let's note the main
things we'll want:

- security
  - we'll want to limit who can read & write
    - -> credential management (XXX: likely needs its own doc)
  - will we want row level security (RLS)?
- visibility
  - if we're running this locally, we'll want to figure out how to expose it
- deployment
  - should we run it locally or remotely, what're the tradeoffs
    - likely a very simple managed instance for us
  - should we use k8s?
- availability / scalability
  - should we put a load balancer in front
- testing
  - how do we test usage in unit-tests? What if we rely on postgresql specifics
    and don't want to have implicit support for sqlite and postgresql?
  - can we run with run_itest for example?
- backup
  - how do we ensure data is preserved properly
  - how do we ensure the disks are all independent?
- migrations
  - how and when are migrations applied or rolled back

## Hackiest Thing

- do most of the management manually
- use GITHUB_SECRETS for the credentials
- no backup or migrations to start
- try managed DB
  - supabase free is IPV6 / github actions is IPV4 :(
