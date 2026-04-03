"""wmariadb - MariaDB ORM using Pydantic models."""

from wmariadb.builders import QueryBuilder
from wmariadb.core.connection import (
    AsyncTransaction,
    AsyncConnectionManager,
    ConnectionManager,
    Transaction,
    get_async_connection,
    get_async_transaction,
    get_connection,
    get_transaction,
    close_global_pools,
)
from wmariadb.core.repository import WMariaDB
from wmariadb.core.sync import AsyncTableSync, TableSync
from wmariadb.exceptions import (
    ConnectionError,
    OperationError,
    SQLInjectionError,
    TableSyncError,
    TransactionError,
    ValidationError,
    WMariaDBError,
)

__version__ = "1.0.0"

__all__ = [
    "WMariaDB",
    "QueryBuilder",
    "ConnectionManager",
    "AsyncConnectionManager",
    "Transaction",
    "AsyncTransaction",
    "get_connection",
    "get_async_connection",
    "get_transaction",
    "get_async_transaction",
    "TableSync",
    "AsyncTableSync",
    "close_global_pools",
    "WMariaDBError",
    "ConnectionError",
    "TableSyncError",
    "ValidationError",
    "OperationError",
    "SQLInjectionError",
    "TransactionError",
]
