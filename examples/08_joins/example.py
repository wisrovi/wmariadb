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


class Order(BaseModel):
    id: int
    user_id: int
    amount: float


def main():
    db_user = WMariaDB(User, DB_CONFIG)
    db_order = WMariaDB(Order, DB_CONFIG)
    db_user.sync.create_if_not_exists()
    db_order.sync.create_if_not_exists()

    db_user.insert(User(id=1, name="John", email="john@example.com"))
    db_order.insert(Order(id=1, user_id=1, amount=100.0))

    query = (
        QueryBuilder()
        .select("u.name", "o.amount")
        .from_table("users", "u")
        .join("orders", "o", "u.id = o.user_id")
        .where("u.id = 1")
        .build()
    )
    print(f"Join query: {query}")

    db_user.close()
    db_order.close()


if __name__ == "__main__":
    main()
