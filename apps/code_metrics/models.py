"""

Structure the tables s.t.
- they aren't largely empty
  - there shouldn't be emergent "patterns" where some are filled and others are
    not, each of those should likely have their own table
  - for example:
    - targets:
      - firmware binary sizes
      - build targets
      - tests
        - success
        - runtime
      - coverage?
        - accumulated from tests
      - dependencies; expected runtime, etc.
    - repo wide (singleton, so likely a single table would suffice for now,
      only separating if it gets too unweildy)

"""

import datetime
import os

import psycopg2  # noqa: F401
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
    # XXX: uniquness may not hold if you have 2 people making this at the exact
    # same time ...
    target_label: orm.Mapped[str] = orm.mapped_column(primary_key=True)

    sha_sum: orm.Mapped[str]
    parent_sha_sum: orm.Mapped[str]
    branch_name: orm.Mapped[str]

    run_created_at: orm.Mapped[datetime.datetime] = orm.mapped_column(
        sqlalchemy.DateTime(timezone=True)
    )
    run_url: orm.Mapped[str] = orm.mapped_column(primary_key=True)

    text: orm.Mapped[int]
    data: orm.Mapped[int]
    bss: orm.Mapped[int]
    # XXX: flash, ram, and max sizes too?

    def __repr__(self) -> str:
        return (
            f"TargetMetrics({self.target_label=}, {self.branch_name=},"
            f" {self.run_url=}, {self.text=}, {self.data=}, {self.bss=})"
        )

    # __table_args__ = (
    #     sqlalchemy.UniqueConstraint('run_url', 'target_label',
    #                                 name='uq_target_run'),
    # )


class RepoMetrics(Base):
    __tablename__ = "repo_metrics"

    sha_sum: orm.Mapped[str]
    parent_sha_sum: orm.Mapped[str]
    branch_name: orm.Mapped[str]

    run_created_at: orm.Mapped[datetime.datetime] = orm.mapped_column(
        sqlalchemy.DateTime(timezone=True)
    )
    run_url: orm.Mapped[str] = orm.mapped_column(primary_key=True)

    # A bit of a toy metric to simply demonstrate an example of a repo-wide
    # metric
    num_files: orm.Mapped[int]


def get_engine() -> sqlalchemy.Engine | None:
    DB_PASSWORD = os.environ.get("DB_PASSWORD")
    if DB_PASSWORD is None:
        return None
    psql_url = (
        f"postgresql://avnadmin:{DB_PASSWORD}@pg-1f58963f-mchristen96-4420"
        ".k.aivencloud.com:15807/defaultdb"
    )
    return sqlalchemy.create_engine(psql_url)


def main():
    engine = get_engine()
    if engine is None:
        return
    # XXX: Use alembic for migrations, etc.
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    main()
