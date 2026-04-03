"""
Test suite for wmariadb library.

Comprehensive tests covering all major functionality.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock


class TestWMariaDBImport:
    """Test basic imports and version."""

    def test_import_main_class(self):
        from wmariadb import WMariaDB

        assert WMariaDB is not None

    def test_import_query_builder(self):
        from wmariadb import QueryBuilder

        assert QueryBuilder is not None

    def test_import_table_sync(self):
        from wmariadb import TableSync

        assert TableSync is not None

    def test_import_transaction(self):
        from wmariadb import Transaction

        assert Transaction is not None

    def test_import_connection_manager(self):
        from wmariadb import ConnectionManager

        assert ConnectionManager is not None

    def test_version(self):
        import wmariadb

        assert wmariadb.__version__ == "1.0.0"


class TestExceptions:
    """Test exception hierarchy."""

    def test_wmariadb_error(self):
        from wmariadb import WMariaDBError

        with pytest.raises(WMariaDBError):
            raise WMariaDBError("test")

    def test_connection_error(self):
        from wmariadb import ConnectionError

        with pytest.raises(ConnectionError):
            raise ConnectionError("test")

    def test_table_sync_error(self):
        from wmariadb import TableSyncError

        with pytest.raises(TableSyncError):
            raise TableSyncError("test")

    def test_validation_error(self):
        from wmariadb import ValidationError

        with pytest.raises(ValidationError):
            raise ValidationError("test")

    def test_operation_error(self):
        from wmariadb import OperationError

        with pytest.raises(OperationError):
            raise OperationError("test")

    def test_sql_injection_error(self):
        from wmariadb import SQLInjectionError

        with pytest.raises(SQLInjectionError):
            raise SQLInjectionError("test")

    def test_transaction_error(self):
        from wmariadb import TransactionError

        with pytest.raises(TransactionError):
            raise TransactionError("test")

    def test_exception_hierarchy(self):
        from wmariadb import (
            WMariaDBError,
            ConnectionError,
            TableSyncError,
            ValidationError,
            OperationError,
            SQLInjectionError,
            TransactionError,
        )

        assert issubclass(ConnectionError, WMariaDBError)
        assert issubclass(TableSyncError, WMariaDBError)
        assert issubclass(ValidationError, WMariaDBError)
        assert issubclass(OperationError, WMariaDBError)
        assert issubclass(SQLInjectionError, WMariaDBError)
        assert issubclass(TransactionError, WMariaDBError)


class TestQueryBuilder:
    """Test QueryBuilder functionality."""

    def test_create_empty_query_builder(self):
        from wmariadb import QueryBuilder

        qb = QueryBuilder("users")
        assert qb is not None
        assert qb.table_name == "users"

    def test_where_equals(self):
        from wmariadb import QueryBuilder

        qb = QueryBuilder("users").where("id", "=", 1)
        query, values = qb.build_select()
        assert "WHERE id = %s" in query
        assert values == (1,)

    def test_where_greater_than(self):
        from wmariadb import QueryBuilder

        qb = QueryBuilder("users").where("age", ">", 18)
        query, values = qb.build_select()
        assert "WHERE age > %s" in query

    def test_where_multiple(self):
        from wmariadb import QueryBuilder

        qb = QueryBuilder("users").where("age", ">", 18).where("city", "=", "NYC")
        query, values = qb.build_select()
        assert "WHERE" in query and "AND" in query
        assert values == (18, "NYC")

    def test_order_by_asc(self):
        from wmariadb import QueryBuilder

        qb = QueryBuilder("users").order_by("name")
        query, _ = qb.build_select()
        assert "ORDER BY name ASC" in query

    def test_order_by_desc(self):
        from wmariadb import QueryBuilder

        qb = QueryBuilder("users").order_by("name", descending=True)
        query, _ = qb.build_select()
        assert "ORDER BY name DESC" in query

    def test_limit(self):
        from wmariadb import QueryBuilder

        qb = QueryBuilder("users").limit(10)
        query, _ = qb.build_select()
        assert "LIMIT 10" in query

    def test_offset(self):
        from wmariadb import QueryBuilder

        qb = QueryBuilder("users").offset(20)
        query, _ = qb.build_select()
        assert "OFFSET 20" in query

    def test_build_count(self):
        from wmariadb import QueryBuilder

        qb = QueryBuilder("users").where("active", "=", True)
        query, values = qb.build_count()
        assert "SELECT COUNT(*)" in query
        assert "WHERE active = %s" in query

    def test_build_delete(self):
        from wmariadb import QueryBuilder

        qb = QueryBuilder("users").where("id", "=", 1)
        query, values = qb.build_delete()
        assert "DELETE FROM users" in query

    def test_reset(self):
        from wmariadb import QueryBuilder

        qb = QueryBuilder("users").where("id", "=", 1).limit(10)
        qb.reset()
        query, values = qb.build_select()
        assert "WHERE" not in query


class TestConnectionManager:
    """Test ConnectionManager class."""

    def test_init(self):
        from wmariadb import ConnectionManager

        cm = ConnectionManager({"host": "localhost", "port": 3306})
        assert cm is not None
        assert cm.min_connections == 1
        assert cm.max_connections == 10

    def test_init_custom_pool(self):
        from wmariadb import ConnectionManager

        cm = ConnectionManager({"host": "localhost"}, min_connections=2, max_connections=20)
        assert cm.min_connections == 2
        assert cm.max_connections == 20

    def test_context_manager(self):
        from wmariadb import ConnectionManager

        cm = ConnectionManager({"host": "localhost"})
        # Just test it can be used as context manager
        assert hasattr(cm, "__enter__")
        assert hasattr(cm, "__exit__")


class TestTableSync:
    """Test TableSync functionality."""

    def test_init(self):
        from wmariadb import TableSync
        from pydantic import BaseModel

        class TestModel(BaseModel):
            id: int
            name: str

        sync = TableSync(TestModel, {"host": "localhost", "dbname": "test"})
        assert sync.table_name == "testmodel"

    def test_sql_type_generation(self):
        from wmariadb.types import get_sql_type
        from pydantic import BaseModel, Field

        class TestModel(BaseModel):
            id: int = Field(..., description="Primary Key")
            name: str = Field(..., description="NOT NULL")
            email: str = Field(None, description="UNIQUE")

        id_type = get_sql_type(TestModel.model_fields["id"])
        name_type = get_sql_type(TestModel.model_fields["name"])
        email_type = get_sql_type(TestModel.model_fields["email"])

        assert "INTEGER" in id_type
        assert "PRIMARY KEY" in id_type
        assert "VARCHAR" in name_type
        assert "NOT NULL" in name_type
        assert "UNIQUE" in email_type
