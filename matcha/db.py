

import sqlite3
import click
import datetime
from flask		import current_app, g
from flask.cli	import with_appcontext
from werkzeug.security import generate_password_hash

# get database descriptor from app config 
def get_db():
	if 'db' not in g:
		g.db = sqlite3.connect(
			current_app.config['DATABASE'],
			detect_types=sqlite3.PARSE_DECLTYPES
		)
		g.db.row_factory = sqlite3.Row
	return g.db


# close database connection
def close_db(e=None):
	db = g.pop('db', None)

	if db is not None:
		db.close()


# initialize database from schema
def init_db():
	db = get_db()

	with current_app.open_resource('schema.sql') as f:
		db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
	'''Clear the existing data and create new tables'''
	init_db()
	click.echo('Initialized the database.')


@click.command('make-admin')
@with_appcontext
def make_admin_command():
	'''Insert default admin user into user table'''
	db = get_db()
	db.execute(
		'INSERT INTO user (username, password, email, last_name, first_name, registered_on, admin, confirmed)'
		' VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
		('admin', generate_password_hash('admin'), 'ad@min.com', 'admin', 'admin', datetime.datetime.now(), True, True)
	)
	db.commit()


def init_app(app):
	app.teardown_appcontext(close_db)
	app.cli.add_command(init_db_command)
	app.cli.add_command(make_admin_command)
