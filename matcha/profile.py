
import os
import functools

from flask import(
	Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app
)

from matcha.db import get_db
from werkzeug.utils import secure_filename


bp = Blueprint('profile', __name__, url_prefix='/profile')


@bp.route('/<username>')
def profile(username):
	error = None
	if request.method == 'POST':
		pass
	db = get_db()
	user = db.execute(
		'SELECT * FROM user WHERE user.username = ?', (username,)
	).fetchone()
	if user is None:
		error = 'User doesn\'t exist'
	if error is not None:
		flash(error)
	return render_template('profile/profile.html', user=user)


@bp.route('/upload_image', methods=('GET', 'POST'))
def upload_image():
	if request.method == 'POST':
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		file = request.files['file']
		# if user does not select file, browser also
		# submit a empty part without filename
		if file.filename == '':
			flash('No selected file')
			return redirect(request.url)
		if file:
			filename = secure_filename(file.filename)
			file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
			return redirect(url_for('index'))

	return render_template('profile/upload_image.html')


