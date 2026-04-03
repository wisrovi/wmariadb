from pydantic import BaseModel
from wmariadb import WMariaDB

DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "password",
    "database": "testdb",
}


class Order(BaseModel):
    id: int
    user_id: int
    amount: float


def main():
    db = WMariaDB(Order, DB_CONFIG)
    db.sync.create_if_not_exists()

    for i in range(1, 6):
        db.insert(Order(id=i, user_id=i, amount=float(i * 10)))

    total = db.aggregate("SUM", "amount")
    print(f"Total amount: {total}")

    count = db.aggregate("COUNT", "id")
    print(f"Order count: {count}")

    avg = db.aggregate("AVG", "amount")
    print(f"Average amount: {avg}")

    db.close()


if __name__ == "__main__":
    main()
