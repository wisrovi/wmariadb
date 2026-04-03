FAQ
===

Frequently Asked Questions about wmariadb.

General
-------

What is wmariadb?
~~~~~~~~~~~~~~~~~

wmariadb is a Python ORM library for MariaDB that uses Pydantic models for type-safe database operations. It provides both synchronous and asynchronous interfaces.

What Python versions are supported?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

wmariadb supports Python 3.9 and later.

What databases are supported?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

wmariadb is designed for MariaDB but also supports MySQL databases through the compatible protocol.

Connection
----------

How do I configure the connection?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use the ``ConnectionManager`` class:

.. code-block:: python

    from wmariadb import ConnectionManager

    cm = ConnectionManager(
        host="localhost",
        port=3306,
        user="your_user",
        password="your_password",
        database="your_database",
        pool_size=5
    )

Can I use connection pooling?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Yes, connection pooling is built-in. Configure pool size in ConnectionManager:

.. code-block:: python

    cm = ConnectionManager(
        host="localhost",
        user="user",
        password="pass",
        database="db",
        pool_size=10,
        max_overflow=20
    )

Models
------

Do I need to define Pydantic models?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

While not strictly required for basic operations, using Pydantic models provides:

- Type validation
- Auto-completion in IDEs
- Schema synchronization
- Data serialization

How do I sync models to the database?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use the ``TableSync`` class:

.. code-block:: python

    from wmariadb import TableSync

    sync = TableSync(cm)
    sync.sync_table(UserModel, "users")

Transactions
------------

How do I use transactions?
~~~~~~~~~~~~~~~~~~~~~~~~~

Use the Transaction context manager:

.. code-block:: python

    from wmariadb import Transaction

    with Transaction(cm) as t:
        db = WMariaDB(t)
        db.insert("table1", data)
        db.insert("table2", data)

Errors
------

What exceptions does wmariadb raise?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

wmariadb provides specific exceptions:

- ``WMariaDBError`` - Base exception
- ``ConnectionError`` - Connection failures
- ``ValidationError`` - Data validation errors
- ``OperationError`` - Database operation errors
- ``TransactionError`` - Transaction failures
- ``SQLInjectionError`` - SQL injection attempts detected