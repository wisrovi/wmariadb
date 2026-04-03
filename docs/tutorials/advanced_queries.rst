Advanced Queries
================

This tutorial covers complex query operations using the QueryBuilder.

Using QueryBuilder
------------------

The QueryBuilder provides a fluent interface for building SQL queries.

Basic Select
~~~~~~~~~~~~

.. code-block:: python

    from wmariadb import QueryBuilder

    query = (QueryBuilder()
        .select("id", "name", "email")
        .from_table("users")
        .build())
    
    results = db.execute(query)

Joins
~~~~~

.. code-block:: python

    query = (QueryBuilder()
        .select("u.id", "u.name", "o.order_id", "o.total")
        .from_table("users", "u")
        .join("orders", "o", "u.id = o.user_id")
        .where("o.status", "=", "completed")
        .build())

Aggregations
~~~~~~~~~~~~

.. code-block:: python

    query = (QueryBuilder()
        .select("COUNT(*)", "AVG(age)", "MAX(age)")
        .from_table("users")
        .build())

Subqueries
~~~~~~~~~~

.. code-block:: python

    query = (QueryBuilder()
        .select("*")
        .from_table("users")
        .where_in("id", 
            QueryBuilder()
            .select("user_id")
            .from_table("orders")
            .where("total", ">", 100)
            .build()
        )
        .build())