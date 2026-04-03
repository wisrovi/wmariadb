from pydantic import BaseModel
from wmariadb import WMariaDB, QueryBuilder

DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "password",
    "database": "testdb",
}


class User(BaseModel):
    id: int
    name: str
    email: str


def main():
    db = WMariaDB(User, DB_CONFIG)
    db.sync.create_if_not_exists()

    db.insert(User(id=1, name="John", email="john@example.com"))
    db.insert(User(id=2, name="Jane", email="jane@example.com"))

    subquery = QueryBuilder().select("MAX(id)").from_table("users").build()
    query = QueryBuilder().select("*").from_table("users").where(f"id = ({subquery})").build()
    print(f"Subquery: {query}")

    db.close()


if __name__ == "__main__":
    main()
