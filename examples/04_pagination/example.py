from pydantic import BaseModel
from wmariadb import WMariaDB

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

    for i in range(1, 21):
        db.insert(User(id=i, name=f"User{i}", email=f"user{i}@example.com"))

    page1 = db.paginate(page=1, page_size=5)
    print(f"Page 1 (5 items): {len(page1)} users")
    print(f"First user: {page1[0].name if page1 else 'none'}")

    page2 = db.paginate(page=2, page_size=5)
    print(f"Page 2 (5 items): {len(page2)} users")

    db.close()


if __name__ == "__main__":
    main()
