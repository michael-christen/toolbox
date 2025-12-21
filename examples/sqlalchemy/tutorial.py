"""Experiment with: https://docs.sqlalchemy.org/en/20/tutorial/index.html."""
import pathlib
from typing import List, Optional

import sqlalchemy
from sqlalchemy import orm


def get_test_engine() -> sqlalchemy.Engine:
    # XXX: :memory was persisting some how
    # return sqlalchemy.create_engine('sqlite+pysqlite:///:memory', echo=True)
    file = "test.db"
    file_path = pathlib.Path(file)
    if file_path.exists():
        file_path.unlink()
    return sqlalchemy.create_engine(f'sqlite+pysqlite:///{file}', echo=True)


def example_query(engine: sqlalchemy.Engine) -> None:
    with engine.connect() as conn:
        # XXX: How to run async?
        result = conn.execute(sqlalchemy.text("select 'hello world'"))
        print(result.all())
        # Must call conn.commit() to commit data


def example_create(engine: sqlalchemy.Engine) -> None:
    with engine.connect() as conn:
        conn.execute(sqlalchemy.text("CREATE TABLE some_table (x int, y int)"))
        conn.execute(
            sqlalchemy.text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
            [{"x": 1, "y": 1}, {"x": 2, "y": 4}],
        )
        conn.commit()
    # OR to avoid the separate commit, open as transaction use engine.begin()
    # instead of engine.connect()


def query_2(engine: sqlalchemy.Engine) -> None:
    with engine.connect() as conn:
        result = conn.execute(sqlalchemy.text("SELECT x, y FROM some_table"))
        for row in result:
            print(f"x: {row.x}  y: {row.y}")
    # OR use a session
    stmt = sqlalchemy.text("SELECT x, y FROM some_table WHERE y > :y ORDER BY x, y")
    with orm.Session(engine) as session:
        session_result = session.execute(stmt, {"y": 1})
        for row in session_result:
            print(f"x: {row.x}  y: {row.y}")


def make_tables(engine: sqlalchemy.Engine) -> None:
    metadata_obj = sqlalchemy.MetaData()

    user_table = sqlalchemy.Table(
        "user_account",
        metadata_obj,
        sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
        sqlalchemy.Column("name", sqlalchemy.String(30)),
        sqlalchemy.Column("fullname", sqlalchemy.String),
    )

    address_table = sqlalchemy.Table(
        "address",
        metadata_obj,
        sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
        sqlalchemy.Column("user_id", sqlalchemy.ForeignKey("user_account.id"), nullable=False),
        sqlalchemy.Column("email_address", sqlalchemy.String, nullable=False),
    )

    # XXX: Use alembic instead
    metadata_obj.create_all(engine)


class Base(orm.DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user_account"
    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    name: orm.Mapped[str] = orm.mapped_column(sqlalchemy.String(30))
    fullname: orm.Mapped[Optional[str]]
    addresses: orm.Mapped[List["Address"]] = orm.relationship(back_populates="user")
    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"

class Address(Base):
    __tablename__ = "address"
    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    email_address: orm.Mapped[str]
    user_id = orm.mapped_column(sqlalchemy.ForeignKey("user_account.id"))
    user: orm.Mapped[User] = orm.relationship(back_populates="addresses")
    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"


def make_table_classes(engine: sqlalchemy.Engine):
    Base.metadata.create_all(engine)


def main():
    # Make a new one
    engine = get_test_engine()
    example_query(engine)
    example_create(engine)
    query_2(engine)
    make_tables(engine)
    make_table_classes(engine)


if __name__ == "__main__":
    main()
