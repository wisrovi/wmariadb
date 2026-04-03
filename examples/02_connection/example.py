from pydantic import BaseModel
from wmariadb import WMariaDB, ConnectionManager

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
    cm = ConnectionManager(**DB_CONFIG)
    with cm.get_connection() as conn:
        print(f"Connected: {conn.is_connected()}")
    cm.close()


if __name__ == "__main__":
    main()
