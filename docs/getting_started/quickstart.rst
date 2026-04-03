Quickstart
===========

This guide will help you get started with wmariadb quickly.

Basic Usage
-----------

Create a model and connect to your database:

.. code-block:: python

    from wmariadb import WMariaDB, ConnectionManager

    # Configure connection
    cm = ConnectionManager(
        host="localhost",
        port=3306,
        user="your_user",
        password="your_password",
        database="your_database"
    )

    # Create repository instance
    db = WMariaDB(cm)

    # Define a Pydantic model
    from pydantic import BaseModel

    class User(BaseModel):
        id: int | None = None
        name: str
        email: str
        age: int | None = None

    # CRUD operations
    user = User(name="John Doe", email="john@example.com", age=30)
    inserted_id = db.insert("users", user)
    
    users = db.select("users", where={"name": "John Doe"})
    
    db.update("users", {"age": 31}, where={"id": inserted_id})
    
    db.delete("users", where={"id": inserted_id})

Async Usage
-----------

For async operations:

.. code-block:: python

    import asyncio
    from wmariadb import AsyncConnectionManager, WMariaDB

    async def main():
        cm = AsyncConnectionManager(
            host="localhost",
            port=3306,
            user="your_user",
            password="your_password",
            database="your_database"
        )

        async with cm:
            db = WMariaDB(cm)
            users = await db.select_async("users")

    asyncio.run(main())

Using QueryBuilder
------------------

Build complex queries programmatically:

.. code-block:: python

    from wmariadb import QueryBuilder

    query = (QueryBuilder()
        .select("id", "name", "email")
        .from_table("users")
        .where("age", ">", 18)
        .order_by("name", "ASC")
        .limit(10)
        .build())

Using TableSync
---------------

Synchronize Pydantic models with database schema:

.. code-block:: python

    from wmariadb import TableSync

    from pydantic import BaseModel

    class User(BaseModel):
        id: int | None = None
        name: str
        email: str

    sync = TableSync(cm)
    sync.sync_table(User, "users")