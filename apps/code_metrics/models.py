import datetime

import sqlalchemy
from sqlalchemy import orm


class Base(orm.DeclarativeBase):
    pass


# Maybe we don't need separate tables?
# class CommitInfo(Base):
#     sha_sum = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
#     parent_sha_sum = sqlalchemy.Column(sqlalchemy.String)
#
#
# class RunInfo(Base):
#     commit_sha_sum = sqlalchemy.Column(sqlalchemy.String)
#     created_at = sqlalchemy.Column(sqlalchemy.DateTime)
#     url = sqlalchemy.Column(sqlalchemy.String, primary_key=True)


# XXX: Use declarative mapping?
# https://docs.sqlalchemy.org/en/20/orm/mapping_styles.html
# XXX: Should we have unique tables per thing
#  - or target and repo metrics; what does growth look like?
# XXX: How do we reduce duplication with serialization / schema formats?
# XXX: Define primary_key constraints
# XXX: Define as tutorial, not this
class TargetMetrics(Base):
    __tablename__ = "target_metrics"
    # XXX: Maybe should add a repo-specifier for the target?
    target_label: orm.Mapped[str]

    sha_sum: orm.Mapped[str]
    parent_sha_sum: orm.Mapped[str]
    branch_name: orm.Mapped[str]

    run_created_at: orm.Mapped[datetime.datetime] = orm.mapped_column(sqlalchemy.DateTime(timezone=True))
    run_url: orm.Mapped[str]

    text: orm.Mapped[int]
    data: orm.Mapped[int]
    bss: orm.Mapped[int]
    # XXX: flash, ram, and max sizes too?


class RepoMetrics(Base):
    __tablename__ = "repo_metrics"

    sha_sum: orm.Mapped[str]
    parent_sha_sum: orm.Mapped[str]
    branch_name: orm.Mapped[str]

    run_created_at: orm.Mapped[datetime.datetime] = orm.mapped_column(sqlalchemy.DateTime(timezone=True))
    run_url: orm.Mapped[str]

    # A bit of a toy metric to simply demonstrate an example of a repo-wide
    # metric
    num_files: orm.Mapped[int]
