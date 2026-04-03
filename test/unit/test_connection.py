import pytest
from wmariadb.core.connection import ConnectionManager


class TestConnectionManager:
    def test_import(self):
        from wmariadb.core.connection import ConnectionManager

        assert ConnectionManager is not None
