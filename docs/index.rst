wmariadb Documentation
=====================

|Version| |License| |Python|

wmariadb is a Python library that provides a high-level interface for MariaDB database operations.
It simplifies database interactions with a clean, intuitive API built on top of pymysql.

.. |Version| image:: https://img.shields.io/pypi/v/wmariadb.svg
   :target: https://pypi.org/project/wmariadb/
   :alt: PyPI Version

.. |License| image:: https://img.shields.io/pypi/l/wmariadb.svg
   :target: https://pypi.org/project/wmariadb/
   :alt: License

.. |Python| image:: https://img.shields.io/pypi/pyversions/wmariadb.svg
   :target: https://pypi.org/project/wmariadb/
   :alt: Python Versions

Quick Start
-----------

.. code-block:: python

   pip install wmariadb

.. code-block:: python

   from wmariadb import MariaDB

   db = MariaDB(host="localhost", user="root", password="pass", database="test")
   result = db.query("SELECT * FROM users WHERE active = true")

Key Capabilities
----------------

- **Connection Management** - Pooled connections with auto-reconnection
- **Query Builder** - Intuitive chainable query builder
- **Type Safety** - Full Pydantic integration for data validation
- **Async Support** - AsyncIO-compatible operations
- **Transaction Support** - Seamless transaction handling

.. toctree::
   :maxdepth: 2
   :caption: Contents

   getting_started/index
   api_reference/index
   tutorials/index
   faq
   glossary

.. toctree::
   :maxdepth: 1
   :caption: Additional

   License <license>
   bibliography

.. toctree::
   :maxdepth: 1
   :caption: External Links

   GitHub <https://github.com/wisrovi/wmariadb>
   PyPI <https://pypi.org/project/wmariadb/>
   LinkedIn <https://www.linkedin.com/in/william-steve-rodriguez-villamizar>

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`