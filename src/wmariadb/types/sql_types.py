from typing import Any


def get_sql_type(field: Any) -> str:
    type_mapping = {int: "INTEGER", str: "VARCHAR(255)", bool: "TINYINT(1)"}
    sql_type = type_mapping.get(field.annotation, "TEXT")
    constraints = []
    description = (field.description or "").lower()
    if "primary" in description:
        constraints.append("PRIMARY KEY")
    if "unique" in description:
        constraints.append("UNIQUE")
    if "not null" in description:
        constraints.append("NOT NULL")
    return f"{sql_type} {' '.join(constraints)}".strip()
