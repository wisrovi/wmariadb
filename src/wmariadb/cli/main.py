import json
import sys

import click
from pydantic import BaseModel

from wmariadb import TableSync, WMariaDB


def load_model(model_path: str) -> type[BaseModel]:
    import importlib.util

    spec = importlib.util.spec_from_file_location("model", model_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    for item in dir(module):
        obj = getattr(module, item)
        if isinstance(obj, type) and issubclass(obj, BaseModel) and obj != BaseModel:
            return obj
    raise ValueError(f"No Pydantic model found in {model_path}")


@click.group()
@click.version_option(version="1.0.0")
def cli():
    """wmariadb - MariaDB ORM CLI tool."""
    pass


@cli.command()
@click.argument("db_config", type=click.Path(exists=True))
@click.argument("model_path", type=click.Path(exists=True))
def init(db_config: str, model_path: str):
    with open(db_config) as f:
        config = json.load(f)
    model = load_model(model_path)
    click.echo(f"Creating table '{model.__name__.lower()}'...")
    sync = TableSync(model, config)
    sync.create_if_not_exists()
    sync.sync_with_model()
    click.echo("Table created successfully!")


@cli.command()
@click.argument("db_config", type=click.Path(exists=True))
@click.argument("model_path", type=click.Path(exists=True))
@click.option("--limit", default=10)
def list(db_config: str, model_path: str, limit: int):
    with open(db_config) as f:
        config = json.load(f)
    model = load_model(model_path)
    db = WMariaDB(model, config)
    for record in db.get_paginated(limit=limit):
        click.echo(record.model_dump())


@cli.command()
@click.argument("db_config", type=click.Path(exists=True))
@click.argument("model_path", type=click.Path(exists=True))
@click.argument("data", type=str)
def insert(db_config: str, model_path: str, data: str):
    with open(db_config) as f:
        config = json.load(f)
    model = load_model(model_path)
    db = WMariaDB(model, config)
    db.insert(model(**json.loads(data)))
    click.echo("Record inserted successfully!")


@cli.command()
@click.argument("db_config", type=click.Path(exists=True))
@click.argument("model_path", type=click.Path(exists=True))
@click.argument("id", type=int)
def get(db_config: str, model_path: str, id: int):
    with open(db_config) as f:
        config = json.load(f)
    model = load_model(model_path)
    db = WMariaDB(model, config)
    records = db.get_by_field(id=id)
    if records:
        click.echo(records[0].model_dump_json(indent=2))
    else:
        click.echo("Record not found", err=True)
        sys.exit(1)


@cli.command()
@click.argument("db_config", type=click.Path(exists=True))
@click.argument("model_path", type=click.Path(exists=True))
@click.argument("id", type=int)
def delete(db_config: str, model_path: str, id: int):
    with open(db_config) as f:
        config = json.load(f)
    model = load_model(model_path)
    db = WMariaDB(model, config)
    db.delete(id)
    click.echo("Record deleted successfully!")


@cli.command()
@click.argument("db_config", type=click.Path(exists=True))
@click.argument("model_path", type=click.Path(exists=True))
def count(db_config: str, model_path: str):
    with open(db_config) as f:
        config = json.load(f)
    model = load_model(model_path)
    db = WMariaDB(model, config)
    click.echo(f"Total records: {db.count()}")


@cli.command()
@click.argument("db_config", type=click.Path(exists=True))
@click.argument("model_path", type=click.Path(exists=True))
def drop(db_config: str, model_path: str):
    with open(db_config) as f:
        config = json.load(f)
    model = load_model(model_path)
    if click.confirm(f"Drop table '{model.__name__.lower()}'?"):
        sync = TableSync(model, config)
        sync.drop_table()
        click.echo("Table dropped!")


if __name__ == "__main__":
    cli()
