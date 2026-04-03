Basic CRUD Operations
======================

This tutorial covers the fundamental Create, Read, Update, and Delete operations using wmariadb.

Prerequisites
-------------

Ensure you have wmariadb installed and a MariaDB database accessible.

Setup
~~~~~

.. code-block:: python

    from wmariadb import WMariaDB, ConnectionManager
    from pydantic import BaseModel

    cm = ConnectionManager(
        host="localhost",
        port=3306,
        user="your_user",
        password="your_password",
        database="your_database"
    )

    db = WMariaDB(cm)

Defining Models
~~~~~~~~~~~~~~~

wmariadb uses Pydantic models to define table schemas:

.. code-block:: python

    class User(BaseModel):
        id: int | None = None
        name: str
        email: str
        age: int | None = None
        created_at: str | None = None

Create (Insert)
~~~~~~~~~~~~~~~

Insert a single record:

.. code-block:: python

    user = User(name="Alice", email="alice@example.com", age=25)
    user_id = db.insert("users", user)
    print(f"Inserted user with ID: {user_id}")

Insert multiple records:

.. code-block:: python

    users = [
        User(name="Bob", email="bob@example.com", age=30),
        User(name="Charlie", email="charlie@example.com", age=35),
    ]
    db.insert_many("users", users)

Read (Select)
~~~~~~~~~~~~~

Select all records:

.. code-block:: python

    all_users = db.select("users")
    for user in all_users:
        print(user)

Select with conditions:

.. code-block:: python

    adults = db.select("users", where={"age": {"operator": ">", "value": 18}})
    print(adults)

Select specific columns:

.. code-block:: python

    names = db.select("users", columns=["name", "email"])

Update
~~~~~~

Update records:

.. code-block:: python

    db.update("users", {"age": 26}, where={"name": "Alice"})

Delete
~~~~~~

Delete records:

.. code-block:: python

    db.delete("users", where={"name": "Alice"})