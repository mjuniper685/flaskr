# db.py - create db requests

import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

# functions to run SQL commands located in schema file

# get_db() returns a database connection
# open_resource() looks for a file relative to the flaskr package
def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

# click.command defines a cli command called init-db, which calls the function below
@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

# this function takes an application and registers close_db and init_db_command
# because of the factory function in init.py this is needed
# this function will be called in the factory function
def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)