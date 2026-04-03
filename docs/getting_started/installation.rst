Installation
============

Requirements
------------

* Python 3.9+
* MariaDB Connector/C or mariadb Python package

Install via pip
---------------

.. code-block:: bash

    pip install wmariadb

Install with development dependencies
-------------------------------------

.. code-block:: bash

    pip install wmariadb[dev]

Install from source
-------------------

.. code-block:: bash

    git clone https://github.com/wisrovi/wmariadb.git
    cd wmariadb
    pip install -e .

Dependencies
~~~~~~~~~~~~

Required dependencies:

* ``pydantic>=2.0.0`` - Data validation and settings management
* ``loguru>=0.7.0`` - Logging library
* ``click>=8.0.0`` - Command-line interface framework

Optional dependencies:

* ``mariadb>=1.1.0`` - MariaDB connector for synchronous operations
* ``aiomysql>=0.2.0`` - Async MySQL/MariaDB driver