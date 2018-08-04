

import os
from flask import Flask, render_template

def create_app(test_config=None):
	#create and configure the app
	matcha = Flask(__name__, instance_relative_config=True)
	matcha.config.from_mapping(
		SECRET_KEY='dev',
		SECURITY_PASSWORD_SALT='my_precious_two',
		DATABASE=os.path.join(matcha.instance_path, 'matcha.sqlite'),
		UPLOAD_FOLDER=os.path.join(matcha.root_path, 'static/images')
	)
	matcha.config.from_pyfile('config.py', silent=True)
	
	try:
		os.makedirs(matcha.instance_path)
	except OSError:
		pass

	@matcha.route('/')
	def hello():
		return 'hello world'

	from . import db
	db.init_app(matcha)

	matcha.add_url_rule('/', endpoint='index')

	from . import auth
	matcha.register_blueprint(auth.bp)
	
	from . import profile
	matcha.register_blueprint(profile.bp)

	
	########################
	#### error handlers ####
	########################

	@matcha.errorhandler(403)
	def forbidden_page(error):
	    return render_template("errors/403.html"), 403


	@matcha.errorhandler(404)
	def page_not_found(error):
	    return render_template("errors/404.html"), 404


	@matcha.errorhandler(500)
	def server_error_page(error):
	    return render_template("errors/500.html"), 500
	
	return matcha

