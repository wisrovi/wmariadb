import logging
from pydantic import BaseModel
from wmariadb import WMariaDB

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

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
    db = WMariaDB(User, DB_CONFIG, log_level=logging.DEBUG)
    db.sync.create_if_not_exists()

    db.insert(User(id=1, name="LoggedUser", email="logged@example.com"))
    print("Operation logged")

    db.close()


if __name__ == "__main__":
    main()
