from pydantic import BaseModel
from wmariadb import WMariaDB

DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "password",
    "database": "testdb",
}


class Product(BaseModel):
    id: int
    name: str
    category: str
    price: float


def main():
    db = WMariaDB(Product, DB_CONFIG)
    db.sync.create_if_not_exists()

    products = [
        Product(id=1, name="Laptop", category="Electronics", price=999.99),
        Product(id=2, name="Mouse", category="Electronics", price=29.99),
        Product(id=3, name="Desk", category="Furniture", price=299.99),
    ]
    for p in products:
        db.insert(p)

    expensive = db.execute_raw(
        "SELECT * FROM products WHERE price > (SELECT AVG(price) FROM products)"
    )
    print(f"Products above average price: {expensive}")

    db.close()


if __name__ == "__main__":
    main()
