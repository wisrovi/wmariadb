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
    query = QueryBuilder().select("*").from_table("users").where("id = 1").build()
    print(query)


if __name__ == "__main__":
    main()
