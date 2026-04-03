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

    users = [User(id=i, name=f"BulkUser{i}", email=f"bulk{i}@example.com") for i in range(1, 11)]
    db.bulk_insert(users)
    print(f"Bulk inserted {len(users)} users")

    db.bulk_update(users)
    print("Bulk updated users")

    all_users = db.get_all()
    print(f"Total users: {len(all_users)}")

    db.close()


if __name__ == "__main__":
    main()
