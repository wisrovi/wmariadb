import pytest
from wmariadb.exceptions import (
    WMariaDBError,
    ConnectionError,
    QueryError,
    ValidationError,
)


class TestExceptions:
    def test_base_error(self):
        with pytest.raises(WMariaDBError):
            raise WMariaDBError("test error")

    def test_connection_error(self):
        with pytest.raises(ConnectionError):
            raise ConnectionError("connection failed")

    def test_query_error(self):
        with pytest.raises(QueryError):
            raise QueryError("query failed")

    def test_validation_error(self):
        with pytest.raises(ValidationError):
            raise ValidationError("validation failed")
