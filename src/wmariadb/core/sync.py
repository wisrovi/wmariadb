import re
from typing import Optional

from wmariadb.core.connection import get_async_connection, get_connection
from wmariadb.types.sql_types import get_sql_type


def validate_identifier(identifier: str) -> None:
    if not re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*$", identifier):
        from wmariadb.exceptions import SQLInjectionError

        raise SQLInjectionError(f"Invalid identifier: {identifier}")


class TableSync:
    def __init__(self, model, db_config: dict):
        self.model = model
        self.db_config = db_config
        self.table_name = model.__name__.lower()

    def create_if_not_exists(self):
        fields = ", ".join(
            f"{field} {get_sql_type(typ)}"
            for field, typ in self.model.model_fields.items()
        )
        query = f"CREATE TABLE IF NOT EXISTS {self.table_name} ({fields})"
        with get_connection(self.db_config) as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()

    def sync_with_model(self):
        query = (
            "SELECT column_name FROM information_schema.columns WHERE table_name = %s"
        )
        with get_connection(self.db_config) as conn:
            cursor = conn.cursor()
            cursor.execute(query, (self.table_name,))
            rows = cursor.fetchall()
            existing_columns = {row[0] for row in rows}
        model_fields = set(self.model.model_fields.keys())
        new_fields = model_fields - existing_columns
        if new_fields:
            with get_connection(self.db_config) as conn:
                cursor = conn.cursor()
                for field in new_fields:
                    field_type = get_sql_type(self.model.model_fields[field])
                    alter_query = (
                        f"ALTER TABLE {self.table_name} ADD COLUMN {field} {field_type}"
                    )
                    cursor.execute(alter_query)
                conn.commit()

    def table_exists(self) -> bool:
        query = "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = %s)"
        with get_connection(self.db_config) as conn:
            cursor = conn.cursor()
            cursor.execute(query, (self.table_name,))
            return cursor.fetchone()[0]

    def drop_table(self):
        query = f"DROP TABLE IF EXISTS {self.table_name}"
        with get_connection(self.db_config) as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()

    def get_columns(self) -> list[str]:
        query = "SELECT column_name FROM information_schema.columns WHERE table_name = %s ORDER BY ordinal_position"
        with get_connection(self.db_config) as conn:
            cursor = conn.cursor()
            cursor.execute(query, (self.table_name,))
            return [row[0] for row in cursor.fetchall()]

    def create_index(
        self, columns: list[str], index_name: Optional[str] = None, unique: bool = False
    ):
        if index_name is None:
            index_name = f"idx_{self.table_name}_{'_'.join(columns)}"
        columns_str = ", ".join(columns)
        unique_str = "UNIQUE " if unique else ""
        query = f"CREATE {unique_str}INDEX IF NOT EXISTS {index_name} ON {self.table_name} ({columns_str})"
        with get_connection(self.db_config) as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()

    def drop_index(self, index_name: str):
        query = f"DROP INDEX IF EXISTS {index_name}"
        with get_connection(self.db_config) as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()

    def get_indexes(self) -> list[dict]:
        query = "SHOW INDEX FROM {self.table_name}"
        with get_connection(self.db_config) as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            return [{"name": row[2], "columns": [row[4]]} for row in cursor.fetchall()]


class AsyncTableSync:
    def __init__(self, model, db_config: dict):
        self.model = model
        self.db_config = db_config
        self.table_name = model.__name__.lower()

    async def create_if_not_exists_async(self):
        fields = ", ".join(
            f"{field} {get_sql_type(typ)}"
            for field, typ in self.model.model_fields.items()
        )
        query = f"CREATE TABLE IF NOT EXISTS {self.table_name} ({fields})"
        conn = await get_async_connection(self.db_config)
        async with conn:
            cursor = await conn.cursor()
            await cursor.execute(query)
            await conn.commit()

    async def sync_with_model_async(self):
        query = (
            "SELECT column_name FROM information_schema.columns WHERE table_name = %s"
        )
        conn = await get_async_connection(self.db_config)
        async with conn:
            cursor = await conn.cursor()
            await cursor.execute(query, (self.table_name,))
            rows = await cursor.fetchall()
            existing_columns = {row[0] for row in rows}
        model_fields = set(self.model.model_fields.keys())
        new_fields = model_fields - existing_columns
        if new_fields:
            conn = await get_async_connection(self.db_config)
            async with conn:
                cursor = await conn.cursor()
                for field in new_fields:
                    field_type = get_sql_type(self.model.model_fields[field])
                    alter_query = (
                        f"ALTER TABLE {self.table_name} ADD COLUMN {field} {field_type}"
                    )
                    await cursor.execute(alter_query)
                await conn.commit()

    async def table_exists_async(self) -> bool:
        query = "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = %s)"
        conn = await get_async_connection(self.db_config)
        async with conn:
            cursor = await conn.cursor()
            await cursor.execute(query, (self.table_name,))
            return (await cursor.fetchone())[0]

    async def drop_table_async(self):
        query = f"DROP TABLE IF EXISTS {self.table_name}"
        conn = await get_async_connection(self.db_config)
        async with conn:
            cursor = await conn.cursor()
            await cursor.execute(query)
            await conn.commit()

    async def get_columns_async(self) -> list[str]:
        query = "SELECT column_name FROM information_schema.columns WHERE table_name = %s ORDER BY ordinal_position"
        conn = await get_async_connection(self.db_config)
        async with conn:
            cursor = await conn.cursor()
            await cursor.execute(query, (self.table_name,))
            return [row[0] for row in await cursor.fetchall()]

    async def create_index_async(
        self, columns: list[str], index_name: Optional[str] = None, unique: bool = False
    ):
        if index_name is None:
            index_name = f"idx_{self.table_name}_{'_'.join(columns)}"
        columns_str = ", ".join(columns)
        unique_str = "UNIQUE " if unique else ""
        query = f"CREATE {unique_str}INDEX IF NOT EXISTS {index_name} ON {self.table_name} ({columns_str})"
        async with get_async_connection(self.db_config) as conn:
            cursor = await conn.cursor()
            await cursor.execute(query)
            await conn.commit()

    async def drop_index_async(self, index_name: str):
        query = f"DROP INDEX IF EXISTS {index_name}"
        async with get_async_connection(self.db_config) as conn:
            cursor = await conn.cursor()
            await cursor.execute(query)
            await conn.commit()

    async def get_indexes_async(self) -> list[dict]:
        query = f"SHOW INDEX FROM {self.table_name}"
        conn = await get_async_connection(self.db_config)
        async with conn:
            cursor = await conn.cursor()
            await cursor.execute(query)
            return [
                {"name": row[2], "columns": [row[4]]} for row in await cursor.fetchall()
            ]
