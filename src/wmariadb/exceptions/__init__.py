class WMariaDBError(Exception):
    pass


class ConnectionError(WMariaDBError):
    pass


class TableSyncError(WMariaDBError):
    pass


class ValidationError(WMariaDBError):
    pass


class OperationError(WMariaDBError):
    pass


class SQLInjectionError(WMariaDBError):
    pass


class TransactionError(WMariaDBError):
    pass


__all__ = [
    "WMariaDBError",
    "ConnectionError",
    "TableSyncError",
    "ValidationError",
    "OperationError",
    "SQLInjectionError",
    "TransactionError",
]
