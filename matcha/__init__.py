

import os
from flask import Flask

def create_app(test_config=None):
	#create and configure the app
	matcha = Flask(__name__, instance_relative_config=True)
	matcha.config.from_mapping(
		SECRET_KEY='dev',
		DATABASE=os.path.join(matcha.instance_path, 'matcha.sqlite'),
	)
	if (test_config) is None:
		matcha.config.from_pyfile('config.py', silent=True)
	else:
		matcha.config.from_mapping(test_config)

	try:
		os.makedirs(matcha.instance_path)
	except OSError:
		pass

	@matcha.route('/')
	def hello():
		return 'hello world!'

	from . import db
	db.init_app(matcha)

	from . import auth
	matcha.register_blueprint(auth.bp)

	matcha.add_url_rule('/', endpoint='index')


	return matcha