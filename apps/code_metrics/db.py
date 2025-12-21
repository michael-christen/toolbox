"""
Example usage:

XXX: get better credential management

with open('aiven_password.txt', 'r') as f:
    password = f.read().strip()

psql_url = (
    f'postgresql://avnadmin:{password}@pg-1f58963f-mchristen96-4420.k.aivencloud.com:15807/defaultdb'
)
engine = sqlalchemy.create_engine(psql_url)

with engine.connect() as conn:
    print('Connection successful')
"""

import sqlalchemy


def get_test_engine() -> sqlalchemy.Engine:
    return sqlalchemy.create_engine("sqlite+pysqlite:///:memory", echo=True)


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
