from pydantic import BaseModel
from wmariadb import WMariaDB, get_transaction

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

    def transaction_operations(tx):
        db.insert(User(id=2, name="Jane", email="jane@example.com"))
        return True

    result = db.with_transaction(transaction_operations)
    print(f"Transaction result: {result}")


if __name__ == "__main__":
    main()
