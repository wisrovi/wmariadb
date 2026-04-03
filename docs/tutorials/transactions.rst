Transactions
============

This tutorial covers transaction management in wmariadb.

Basic Transactions
------------------

Use the Transaction context manager for atomic operations:

.. code-block:: python

    from wmariadb import WMariaDB, ConnectionManager, Transaction

    cm = ConnectionManager(
        host="localhost",
        port=3306,
        user="your_user",
        password="your_password",
        database="your_database"
    )

    with Transaction(cm) as t:
        db = WMariaDB(t)
        
        db.insert("accounts", {"id": 1, "balance": 1000})
        db.insert("accounts", {"id": 2, "balance": 500})
        
        db.execute("UPDATE accounts SET balance = balance - 100 WHERE id = 1")
        db.execute("UPDATE accounts SET balance = balance + 100 WHERE id = 2")

Commit and Rollback
~~~~~~~~~~~~~~~~~~~

Transactions automatically commit on success:

.. code-block:: python

    with Transaction(cm) as t:
        db = WMariaDB(t)
        db.insert("logs", {"action": "test"})
    # Committed automatically

For manual control:

.. code-block:: python

    from wmariadb import Transaction

    t = Transaction(cm)
    try:
        db = WMariaDB(t)
        db.insert("data", {"value": "test"})
        t.commit()
    except Exception as e:
        t.rollback()
        raise e

Async Transactions
-----------------

.. code-block:: python

    import asyncio
    from wmariadb import AsyncTransaction, WMariaDB, AsyncConnectionManager

    async def main():
        cm = AsyncConnectionManager(
            host="localhost",
            user="your_user",
            password="your_password",
            database="your_database"
        )

        async with AsyncTransaction(cm) as t:
            db = WMariaDB(t)
            await db.insert_async("logs", {"action": "async_test"})

    asyncio.run(main())