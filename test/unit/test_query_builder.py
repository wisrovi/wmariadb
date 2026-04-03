import pytest
from wmariadb.builders.query_builder import QueryBuilder


class TestQueryBuilder:
    def test_select(self):
        qb = QueryBuilder()
        result = qb.select("*").from_table("users").build()
        assert "SELECT * FROM users" in result

    def test_insert(self):
        qb = QueryBuilder()
        result = qb.insert("users", {"id": 1, "name": "test"}).build()
        assert "INSERT INTO users" in result

    def test_update(self):
        qb = QueryBuilder()
        result = qb.update("users", {"name": "test"}).where("id", 1).build()
        assert "UPDATE users" in result

    def test_delete(self):
        qb = QueryBuilder()
        result = qb.delete("users").where("id", 1).build()
        assert "DELETE FROM users" in result
