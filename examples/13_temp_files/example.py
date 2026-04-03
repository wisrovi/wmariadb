import os
import tempfile
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

    temp_file = tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt")
    temp_file.write("Temp data\n")
    temp_file.close()

    db.insert(User(id=1, name="TempUser", email="temp@example.com"))
    users = db.get_all()
    print(f"Users: {len(users)}")

    os.unlink(temp_file.name)
    db.close()


if __name__ == "__main__":
    main()
