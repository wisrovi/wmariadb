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
    db.insert(User(id=1, name="John", email="john@example.com"))
    users = db.get_all()
    print(users)
    db.close()


if __name__ == "__main__":
    main()
