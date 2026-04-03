Glossary
========

This glossary defines key terms used throughout the wmariadb documentation.

.. glossary::
   :sorted:

   ORM
      Object-Relational Mapping. A technique that maps database tables to Python objects, allowing developers to work with databases using Python code.

   Pydantic
      A Python data validation library used by wmariadb to define schema models with type hints.

   Connection Manager
      A class that manages database connections, including connection pooling and lifecycle.

   Query Builder
      A fluent interface for constructing SQL queries programmatically without writing raw SQL.

   Transaction
      A sequence of database operations that are executed as a single atomic unit.

   Table Sync
      A feature that synchronizes Pydantic model definitions with database table schemas.

   CRUD
      Create, Read, Update, Delete - the four basic operations of persistent storage.

   Pool Size
      The maximum number of connections maintained in the connection pool.

   Async
      Asynchronous programming pattern using Python's async/await syntax for non-blocking operations.

   Repository Pattern
      A design pattern that abstracts data access logic, providing a clean interface for database operations.