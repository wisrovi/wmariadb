from pydantic import BaseModel
from wmariadb import WMariaDB

DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "password",
    "database": "testdb",
}


class Employee(BaseModel):
    id: int
    name: str
    department: str
    salary: float


def main():
    db = WMariaDB(Employee, DB_CONFIG)
    db.sync.create_if_not_exists()

    employees = [
        Employee(id=1, name="Alice", department="IT", salary=70000),
        Employee(id=2, name="Bob", department="IT", salary=75000),
        Employee(id=3, name="Charlie", department="HR", salary=65000),
    ]
    for emp in employees:
        db.insert(emp)

    result = db.execute_raw(
        "SELECT name, department, salary, ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) as rn FROM employees"
    )
    print(f"Window function result: {result}")

    db.close()


if __name__ == "__main__":
    main()
