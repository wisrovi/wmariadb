"""Connection management for MariaDB with automatic connection pooling."""

import logging
import threading
from contextlib import contextmanager
from typing import Any, Optional

logger = logging.getLogger(__name__)

_global_pool_lock = threading.Lock()
_global_sync_pool: Optional[Any] = None
_global_async_pool: Optional[Any] = None
_default_pool_config = {"min_size": 2, "max_size": 20}


def _build_conninfo(db_config: dict) -> str:
    """Build connection string from config dict."""
    try:
        import mariadb

        return {
            "host": db_config.get("host", "localhost"),
            "port": db_config.get("port", 3306),
            "user": db_config.get("user", "root"),
            "password": db_config.get("password", ""),
            "database": db_config.get("dbname", db_config.get("database", "")),
        }
    except ImportError:
        return f"{db_config.get('user', 'root')}:{db_config.get('password', '')}@{db_config.get('host', 'localhost')}:{db_config.get('port', 3306)}/{db_config.get('dbname', '')}"


def _get_global_sync_pool(db_config: dict) -> Any:
    """Get or create global sync connection pool."""
    global _global_sync_pool

    try:
        from mariadb.pool import ConnectionPool
    except ImportError:
        return None

    conninfo = _build_conninfo(db_config)

    with _global_pool_lock:
        if _global_sync_pool is None:
            try:
                _global_sync_pool = ConnectionPool(
                    pool_name="wmariadb_pool",
                    pool_size=_default_pool_config["max_size"],
                    **conninfo,
                )
                logger.info(f"Created global sync pool")
            except Exception as e:
                logger.warning(f"Could not create pool: {e}")
                return None
        return _global_sync_pool


def _get_global_async_pool(db_config: dict) -> Any:
    """Get or create global async connection pool."""
    global _global_async_pool

    with _global_pool_lock:
        if _global_async_pool is None:
            logger.info(f"Created global async pool")
        return _global_async_pool


def close_global_pools():
    """Close global connection pools."""
    global _global_sync_pool, _global_async_pool

    with _global_pool_lock:
        if _global_sync_pool:
            _global_sync_pool = None
        if _global_async_pool:
            _global_async_pool = None
        logger.info("Global connection pools closed")


class _PooledConnection:
    """Wrapper for pooled connection that returns to pool on close."""

    def __init__(self, conn: Any, pool: Any):
        self._conn = conn
        self._pool = pool

    def __enter__(self):
        return self._conn

    def __exit__(self, *args):
        if self._conn:
            self._pool.putconn(self._conn)
        return False

    def __getattr__(self, name):
        return getattr(self._conn, name)


class Transaction:
    """Context manager for database transactions (sync)."""

    def __init__(self, db_config: dict):
        self.db_config = db_config
        self.conn: Optional[Any] = None
        self._committed = False

    def __enter__(self):
        try:
            import mariadb

            self.conn = mariadb.connect(**_build_conninfo(self.db_config))
            self.conn.autocommit = False
        except ImportError:
            import pymysql

            self.conn = pymysql.connect(
                **{
                    "host": self.db_config.get("host", "localhost"),
                    "port": self.db_config.get("port", 3306),
                    "user": self.db_config.get("user", "root"),
                    "password": self.db_config.get("password", ""),
                    "database": self.db_config.get("dbname", ""),
                }
            )
            self.conn.autocommit = False
        logger.debug("Transaction started")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.conn.rollback()
            logger.debug("Transaction rolled back")
        elif not self._committed:
            self.conn.commit()
            logger.debug("Transaction committed")
        self.conn.close()
        return False

    def commit(self):
        self.conn.commit()
        self._committed = True

    def rollback(self):
        self.conn.rollback()

    def execute(self, query: str, values: tuple = None) -> Any:
        cursor = self.conn.cursor()
        cursor.execute(query, values or ())
        if cursor.description:
            return cursor.fetchall()
        return cursor.rowcount


class AsyncTransaction:
    """Context manager for database transactions (async)."""

    def __init__(self, db_config: dict):
        self.db_config = db_config
        self.conn: Optional[Any] = None
        self._committed = False

    async def __aenter__(self):
        try:
            import mariadb

            self.conn = await mariadb.connect(**_build_conninfo(self.db_config))
        except ImportError:
            import aiomysql

            self.conn = await aiomysql.connect(
                host=self.db_config.get("host", "localhost"),
                port=self.db_config.get("port", 3306),
                user=self.db_config.get("user", "root"),
                password=self.db_config.get("password", ""),
                db=self.db_config.get("dbname", ""),
            )
        self.conn.autocommit = False
        logger.debug("Async transaction started")
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            await self.conn.rollback()
            logger.debug("Async transaction rolled back")
        elif not self._committed:
            await self.conn.commit()
            logger.debug("Async transaction committed")
        await self.conn.close()
        return False

    async def commit(self):
        await self.conn.commit()
        self._committed = True

    async def rollback(self):
        await self.conn.rollback()

    async def execute(self, query: str, values: tuple = None) -> Any:
        cursor = await self.conn.cursor()
        await cursor.execute(query, values or ())
        if cursor.description:
            return await cursor.fetchall()
        return cursor.rowcount


@contextmanager
def get_transaction(db_config: dict):
    """Get a transaction context manager (sync)."""
    transaction = Transaction(db_config)
    yield transaction


@contextmanager
async def get_async_transaction(db_config: dict):
    """Get an async transaction context manager."""
    transaction = AsyncTransaction(db_config)
    async with transaction:
        yield transaction


class ConnectionManager:
    """Manages MariaDB database connections (sync)."""

    def __init__(
        self, db_config: dict, min_connections: int = 1, max_connections: int = 10
    ):
        self.db_config = db_config
        self.min_connections = min_connections
        self.max_connections = max_connections
        self._pool: Optional[Any] = None

    def get_connection(self) -> Any:
        if self._pool is None:
            try:
                from mariadb.pool import ConnectionPool

                conninfo = _build_conninfo(self.db_config)
                self._pool = ConnectionPool(
                    pool_name="wmariadb_pool",
                    pool_size=self.max_connections,
                    **conninfo,
                )
            except ImportError:
                return None
        return self._pool.getconn()

    def release_connection(self, conn: Any):
        if self._pool:
            self._pool.putconn(conn)

    def close_all(self):
        if self._pool:
            self._pool = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_all()


class AsyncConnectionManager:
    """Manages MariaDB database connections (async)."""

    def __init__(
        self, db_config: dict, min_connections: int = 1, max_connections: int = 10
    ):
        self.db_config = db_config
        self.min_connections = min_connections
        self.max_connections = max_connections

    async def get_connection(self) -> Any:
        try:
            import mariadb

            return await mariadb.connect(**_build_conninfo(self.db_config))
        except ImportError:
            import aiomysql

            return await aiomysql.connect(
                host=self.db_config.get("host", "localhost"),
                port=self.db_config.get("port", 3306),
                user=self.db_config.get("user", "root"),
                password=self.db_config.get("password", ""),
                db=self.db_config.get("dbname", ""),
            )

    async def close_all(self):
        pass


def get_connection(db_config: dict) -> _PooledConnection:
    """Get a connection from global pool (sync)."""
    try:
        pool = _get_global_sync_pool(db_config)
        conn = pool.getconn()
        return _PooledConnection(conn, pool)
    except Exception as e:
        logger.error(f"Failed to get connection: {e}")
        raise


async def get_async_connection(db_config: dict) -> Any:
    """Get a connection from global pool (async)."""
    try:
        import mariadb

        return await mariadb.connect(**_build_conninfo(db_config))
    except ImportError:
        import aiomysql

        return await aiomysql.connect(
            host=db_config.get("host", "localhost"),
            port=db_config.get("port", 3306),
            user=db_config.get("user", "root"),
            password=db_config.get("password", ""),
            db=db_config.get("dbname", ""),
        )
