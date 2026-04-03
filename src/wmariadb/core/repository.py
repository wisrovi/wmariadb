"""Main repository class for MariaDB operations."""

import logging
import re
from typing import Any, Callable, Optional

from pydantic import BaseModel

from wmariadb.core.connection import (
    AsyncTransaction,
    Transaction,
    get_async_connection,
    get_connection,
    get_transaction,
)
from wmariadb.core.sync import AsyncTableSync, TableSync
from wmariadb.exceptions import SQLInjectionError, TransactionError

logger = logging.getLogger(__name__)


def validate_identifier(identifier: str) -> None:
    """Validate SQL identifier to prevent SQL injection."""
    if not re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*$", identifier):
        raise SQLInjectionError(f"Invalid identifier: {identifier}")


class WMariaDB:
    """MariaDB repository using Pydantic models."""

    def __init__(self, model: type[BaseModel], db_config: dict):
        self.model = model
        self.db_config = db_config
        self.table_name = model.__name__.lower()
        self._sync = TableSync(model, db_config)

        self._sync.create_if_not_exists()
        self._sync.sync_with_model()

    def insert(self, data: BaseModel) -> None:
        """Insert a new record into the database."""
        data_dict = data.model_dump()
        fields = ", ".join(data_dict.keys())
        placeholders = ", ".join(["%s"] * len(data_dict))
        values = tuple(data_dict.values())

        query = f"INSERT INTO {self.table_name} ({fields}) VALUES ({placeholders})"
        with get_connection(self.db_config) as conn:
            cursor = conn.cursor()
            cursor.execute(query, values)
            conn.commit()

    def get_all(self) -> list[BaseModel]:
        """Get all records from the table."""
        query = f"SELECT * FROM {self.table_name}"
        with get_connection(self.db_config) as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()

        return [
            self.model(
                **{
                    key: (value if value is not None else self._default_value(key))
                    for key, value in zip(self.model.model_fields.keys(), row)
                }
            )
            for row in rows
        ]

    def get_by_field(self, **filters) -> list[BaseModel]:
        """Get records filtered by specified fields."""
        if not filters:
            return self.get_all()

        conditions = " AND ".join(f"{key} = %s" for key in filters)
        values = tuple(filters.values())
        query = f"SELECT * FROM {self.table_name} WHERE {conditions}"

        with get_connection(self.db_config) as conn:
            cursor = conn.cursor()
            cursor.execute(query, values)
            rows = cursor.fetchall()

        return [
            self.model(
                **{
                    key: (value if value is not None else self._default_value(key))
                    for key, value in zip(self.model.model_fields.keys(), row)
                }
            )
            for row in rows
        ]

    def update(self, record_id: int, data: BaseModel) -> None:
        """Update a record in the database."""
        data_dict = data.model_dump()
        fields = ", ".join(f"{key} = %s" for key in data_dict.keys())
        values = tuple(data_dict.values()) + (record_id,)
        query = f"UPDATE {self.table_name} SET {fields} WHERE id = %s"

        with get_connection(self.db_config) as conn:
            cursor = conn.cursor()
            cursor.execute(query, values)
            conn.commit()

    def delete(self, record_id: int) -> None:
        """Delete a record from the database."""
        query = f"DELETE FROM {self.table_name} WHERE id = %s"
        with get_connection(self.db_config) as conn:
            cursor = conn.cursor()
            cursor.execute(query, (record_id,))
            conn.commit()

    def _default_value(self, field: str) -> Any:
        field_type = self.model.model_fields[field].annotation
        if field_type is str:
            return ""
        elif field_type is int:
            return 0
        elif field_type is bool:
            return False
        return None

    def get_paginated(
        self,
        limit: int = 10,
        offset: int = 0,
        order_by: Optional[str] = None,
        order_desc: bool = False,
    ) -> list[BaseModel]:
        validate_identifier(self.table_name)
        if order_by:
            validate_identifier(order_by)
            order_clause = f" ORDER BY {order_by} {'DESC' if order_desc else 'ASC'}"
        else:
            order_clause = ""

        query = f"SELECT * FROM {self.table_name}{order_clause} LIMIT %s OFFSET %s"
        with get_connection(self.db_config) as conn:
            cursor = conn.cursor()
            cursor.execute(query, (limit, offset))
            rows = cursor.fetchall()

        return [
            self.model(
                **{
                    key: (value if value is not None else self._default_value(key))
                    for key, value in zip(self.model.model_fields.keys(), row)
                }
            )
            for row in rows
        ]

    def get_page(self, page: int = 1, per_page: int = 10) -> list[BaseModel]:
        if page < 1:
            page = 1
        if per_page < 1:
            per_page = 10
        offset = (page - 1) * per_page
        return self.get_paginated(limit=per_page, offset=offset)

    def count(self) -> int:
        validate_identifier(self.table_name)
        query = f"SELECT COUNT(*) FROM {self.table_name}"
        with get_connection(self.db_config) as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            result = cursor.fetchone()
        return result[0] if result else 0

    def insert_many(self, data_list: list[BaseModel]) -> None:
        if not data_list:
            return
        data_dicts = [data.model_dump() for data in data_list]
        fields = ", ".join(data_dicts[0].keys())
        placeholders = ", ".join(["%s"] * len(data_dicts[0]))
        query = f"INSERT INTO {self.table_name} ({fields}) VALUES ({placeholders})"
        with get_connection(self.db_config) as conn:
            cursor = conn.cursor()
            for data_dict in data_dicts:
                values = tuple(data_dict.values())
                cursor.execute(query, values)
            conn.commit()

    def update_many(self, updates: list[tuple[BaseModel, int]]) -> int:
        if not updates:
            return 0
        validate_identifier(self.table_name)
        total_updated = 0
        with get_connection(self.db_config) as conn:
            cursor = conn.cursor()
            for data, record_id in updates:
                data_dict = data.model_dump()
                fields = ", ".join(f"{key} = %s" for key in data_dict)
                values = tuple(data_dict.values()) + (record_id,)
                query = f"UPDATE {self.table_name} SET {fields} WHERE id = %s"
                cursor.execute(query, values)
                total_updated += cursor.rowcount
            conn.commit()
        return total_updated

    def delete_many(self, record_ids: list[int]) -> int:
        if not record_ids:
            return 0
        validate_identifier(self.table_name)
        with get_connection(self.db_config) as conn:
            cursor = conn.cursor()
            for record_id in record_ids:
                query = f"DELETE FROM {self.table_name} WHERE id = %s"
                cursor.execute(query, (record_id,))
            conn.commit()
        return len(record_ids)

    def execute_transaction(self, operations: list[tuple[str, tuple]]) -> list[Any]:
        results = []
        try:
            with get_transaction(self.db_config) as txn:
                for query, values in operations:
                    result = txn.execute(query, values)
                    if result is not None:
                        results.append(result)
                txn.commit()
                logger.info(f"Transaction completed with {len(operations)} operations")
        except Exception as e:
            logger.error(f"Transaction failed: {e}")
            raise TransactionError(f"Transaction failed: {e}") from e
        return results

    def with_transaction(self, func: Callable[[Transaction], Any]) -> Any:
        try:
            with get_transaction(self.db_config) as txn:
                result = func(txn)
                txn.commit()
                logger.info("Transaction completed successfully")
                return result
        except Exception as e:
            logger.error(f"Transaction failed: {e}")
            raise TransactionError(f"Transaction failed: {e}") from e

    async def insert_async(self, data: BaseModel) -> None:
        data_dict = data.model_dump()
        fields = ", ".join(data_dict.keys())
        placeholders = ", ".join(["%s"] * len(data_dict))
        values = tuple(data_dict.values())
        query = f"INSERT INTO {self.table_name} ({fields}) VALUES ({placeholders})"
        conn = await get_async_connection(self.db_config)
        async with conn:
            cursor = await conn.cursor()
            await cursor.execute(query, values)
            await conn.commit()

    async def get_all_async(self) -> list[BaseModel]:
        query = f"SELECT * FROM {self.table_name}"
        conn = await get_async_connection(self.db_config)
        async with conn:
            cursor = await conn.cursor()
            await cursor.execute(query)
            rows = await cursor.fetchall()
        return [
            self.model(
                **{
                    key: (value if value is not None else self._default_value(key))
                    for key, value in zip(self.model.model_fields.keys(), row)
                }
            )
            for row in rows
        ]

    async def get_by_field_async(self, **filters) -> list[BaseModel]:
        if not filters:
            return await self.get_all_async()
        conditions = " AND ".join(f"{key} = %s" for key in filters)
        values = tuple(filters.values())
        query = f"SELECT * FROM {self.table_name} WHERE {conditions}"
        conn = await get_async_connection(self.db_config)
        async with conn:
            cursor = await conn.cursor()
            await cursor.execute(query, values)
            rows = await cursor.fetchall()
        return [
            self.model(
                **{
                    key: (value if value is not None else self._default_value(key))
                    for key, value in zip(self.model.model_fields.keys(), row)
                }
            )
            for row in rows
        ]

    async def update_async(self, record_id: int, data: BaseModel) -> None:
        data_dict = data.model_dump()
        fields = ", ".join(f"{key} = %s" for key in data_dict)
        values = tuple(data_dict.values()) + (record_id,)
        query = f"UPDATE {self.table_name} SET {fields} WHERE id = %s"
        conn = await get_async_connection(self.db_config)
        async with conn:
            cursor = await conn.cursor()
            await cursor.execute(query, values)
            await conn.commit()

    async def delete_async(self, record_id: int) -> None:
        query = f"DELETE FROM {self.table_name} WHERE id = %s"
        conn = await get_async_connection(self.db_config)
        async with conn:
            cursor = await conn.cursor()
            await cursor.execute(query, (record_id,))
            await conn.commit()

    async def get_paginated_async(
        self,
        limit: int = 10,
        offset: int = 0,
        order_by: Optional[str] = None,
        order_desc: bool = False,
    ) -> list[BaseModel]:
        validate_identifier(self.table_name)
        if order_by:
            validate_identifier(order_by)
            order_clause = f" ORDER BY {order_by} {'DESC' if order_desc else 'ASC'}"
        else:
            order_clause = ""
        query = f"SELECT * FROM {self.table_name}{order_clause} LIMIT %s OFFSET %s"
        conn = await get_async_connection(self.db_config)
        async with conn:
            cursor = await conn.cursor()
            await cursor.execute(query, (limit, offset))
            rows = await cursor.fetchall()
        return [
            self.model(
                **{
                    key: (value if value is not None else self._default_value(key))
                    for key, value in zip(self.model.model_fields.keys(), row)
                }
            )
            for row in rows
        ]

    async def get_page_async(self, page: int = 1, per_page: int = 10) -> list[BaseModel]:
        if page < 1:
            page = 1
        if per_page < 1:
            per_page = 10
        offset = (page - 1) * per_page
        return await self.get_paginated_async(limit=per_page, offset=offset)

    async def count_async(self) -> int:
        validate_identifier(self.table_name)
        query = f"SELECT COUNT(*) FROM {self.table_name}"
        conn = await get_async_connection(self.db_config)
        async with conn:
            cursor = await conn.cursor()
            await cursor.execute(query)
            result = await cursor.fetchone()
        return result[0] if result else 0

    async def insert_many_async(self, data_list: list[BaseModel]) -> None:
        if not data_list:
            return
        data_dicts = [data.model_dump() for data in data_list]
        fields = ", ".join(data_dicts[0].keys())
        placeholders = ", ".join(["%s"] * len(data_dicts[0]))
        query = f"INSERT INTO {self.table_name} ({fields}) VALUES ({placeholders})"
        conn = await get_async_connection(self.db_config)
        async with conn:
            cursor = await conn.cursor()
            for data_dict in data_dicts:
                values = tuple(data_dict.values())
                await cursor.execute(query, values)
            await conn.commit()

    async def update_many_async(self, updates: list[tuple[BaseModel, int]]) -> int:
        if not updates:
            return 0
        validate_identifier(self.table_name)
        total_updated = 0
        conn = await get_async_connection(self.db_config)
        async with conn:
            cursor = await conn.cursor()
            for data, record_id in updates:
                data_dict = data.model_dump()
                fields = ", ".join(f"{key} = %s" for key in data_dict)
                values = tuple(data_dict.values()) + (record_id,)
                query = f"UPDATE {self.table_name} SET {fields} WHERE id = %s"
                await cursor.execute(query, values)
                total_updated += cursor.rowcount
            await conn.commit()
        return total_updated

    async def delete_many_async(self, record_ids: list[int]) -> int:
        if not record_ids:
            return 0
        validate_identifier(self.table_name)
        conn = await get_async_connection(self.db_config)
        async with conn:
            cursor = await conn.cursor()
            for record_id in record_ids:
                query = f"DELETE FROM {self.table_name} WHERE id = %s"
                await cursor.execute(query, (record_id,))
            await conn.commit()
        return len(record_ids)

    async def execute_transaction_async(self, operations: list[tuple[str, tuple]]) -> list[Any]:
        results = []
        try:
            conn = await get_async_connection(self.db_config)
            async with conn:
                cursor = await conn.cursor()
                for query, values in operations:
                    await cursor.execute(query, values)
                    if cursor.description:
                        result = await cursor.fetchall()
                        results.append(result)
                await conn.commit()
                logger.info(f"Async transaction completed with {len(operations)} operations")
        except Exception as e:
            logger.error(f"Async transaction failed: {e}")
            raise TransactionError(f"Async transaction failed: {e}") from e
        return results

    async def with_transaction_async(self, func: Callable[[AsyncTransaction], Any]) -> Any:
        try:
            conn = await get_async_connection(self.db_config)
            async with conn:
                txn = AsyncTransaction(self.db_config)
                txn.conn = conn
                result = await func(txn)
                await txn.commit()
                logger.info("Async transaction completed successfully")
                return result
        except Exception as e:
            logger.error(f"Async transaction failed: {e}")
            raise TransactionError(f"Async transaction failed: {e}") from e
