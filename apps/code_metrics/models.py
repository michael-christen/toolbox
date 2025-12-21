import sqlalchemy

# from sqlalchemy import orm

Base = sqlalchemy.declarative_base()


class CommitInfo(Base):
    sha_sum = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    parent_sha_sum = sqlalchemy.Column(sqlalchemy.String)


# Maybe we don't need separate tables?
class RunInfo(Base):
    commit_sha_sum = sqlalchemy.Column(sqlalchemy.String)
    created_at = sqlalchemy.Column(sqlalchemy.DateTime)
    url = sqlalchemy.Column(sqlalchemy.String, primary_key=True)


# XXX: Use declarative mapping?
# https://docs.sqlalchemy.org/en/20/orm/mapping_styles.html
# XXX: Should we have unique tables per thing
#  - or target and repo metrics; what does growth look like?
# XXX: How do we reduce duplication with serialization / schema formats?
# XXX: Define primary_key constraints
# XXX: Define as tutorial, not this
class TargetMetrics(Base):
    # XXX: Maybe should add a repo-specifier for the target?
    target_label = sqlalchemy.Column(sqlalchemy.String)

    sha_sum = sqlalchemy.Column(sqlalchemy.String)
    parent_sha_sum = sqlalchemy.Column(sqlalchemy.String)
    branch_name = sqlalchemy.Column(sqlalchemy.String)

    run_created_at = sqlalchemy.Column(sqlalchemy.DateTime)
    run_url = sqlalchemy.Column(sqlalchemy.String)

    text = sqlalchemy.Column(sqlalchemy.Int)
    data = sqlalchemy.Column(sqlalchemy.Int)
    bss = sqlalchemy.Column(sqlalchemy.Int)
    # XXX: flash, ram, and max sizes too?


class RepoMetrics(Base):
    sha_sum = sqlalchemy.Column(sqlalchemy.String)
    parent_sha_sum = sqlalchemy.Column(sqlalchemy.String)
    branch_name = sqlalchemy.Column(sqlalchemy.String)

    run_created_at = sqlalchemy.Column(sqlalchemy.DateTime)
    run_url = sqlalchemy.Column(sqlalchemy.String)

    # A bit of a toy metric to simply demonstrate an example of a repo-wide
    # metric
    num_files = sqlalchemy.Column(sqlalchemy.Int)
