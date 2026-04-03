Async Usage
===========

This tutorial covers asynchronous operations in wmariadb.

Setup Async Connection
---------------------

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
            # Use async methods
            users = await db.select_async("users")

    asyncio.run(main())

Async CRUD Operations
--------------------

Insert:

.. code-block:: python

    user = {"name": "Alice", "email": "alice@example.com"}
    user_id = await db.insert_async("users", user)

Select:

.. code-block:: python

    users = await db.select_async("users", where={"age": {"operator": ">", "value": 18}})

Update:

.. code-block:: python

    await db.update_async("users", {"age": 26}, where={"name": "Alice"})

Delete:

.. code-block:: python

    await db.delete_async("users", where={"id": user_id})

Async QueryBuilder
------------------

.. code-block:: python

    from wmariadb import QueryBuilder

    async def fetch_users():
        query = (QueryBuilder()
            .select("*")
            .from_table("users")
            .where("active", "=", True)
            .build())

        results = await db.execute_async(query)
        return results

Using AsyncTableSync
--------------------

.. code-block:: python

    import asyncio
    from wmariadb import AsyncTableSync
    from pydantic import BaseModel

    class User(BaseModel):
        id: int | None = None
        name: str
        email: str

    async def main():
        sync = AsyncTableSync(cm)
        await sync.sync_table_async(User, "users")

    asyncio.run(main())