import pytest


class TestWMariaDBImport:
    def test_import(self):
        from wmariadb import WMariaDB

        assert WMariaDB is not None

    def test_version(self):
        import wmariadb

        assert wmariadb.__version__ == "1.0.0"


class TestQueryBuilder:
    def test_import(self):
        from wmariadb import QueryBuilder

        qb = QueryBuilder("users")
        assert qb.table_name == "users"

    def test_where(self):
        from wmariadb import QueryBuilder

        qb = QueryBuilder("users").where("id", "=", 1)
        query, values = qb.build_select()
        assert "WHERE id = %s" in query
        assert values == (1,)


class TestExceptions:
    def test_import(self):
        from wmariadb import WMariaDBError

        with pytest.raises(WMariaDBError):
            raise WMariaDBError("test")
