import pytest
from wmariadb.types.sql_types import map_pydantic_to_sql


class TestSQLTypes:
    def test_map_int(self):
        result = map_pydantic_to_sql("int")
        assert result is not None

    def test_map_str(self):
        result = map_pydantic_to_sql("str")
        assert result is not None

    def test_map_float(self):
        result = map_pydantic_to_sql("float")
        assert result is not None
