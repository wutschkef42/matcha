
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
	images = db.execute(
		'SELECT * FROM image WHERE image.profile_id = ?', (user['id'],)
	).fetchall()
	if user is None:
		error = 'User doesn\'t exist'
	if error is not None:
		flash(error)
	return render_template('profile/profile.html', user=user, images=images)


@bp.route('/<username>/upload_image', methods=('GET', 'POST'))
def upload_image(username):
	if request.method == 'POST':
		db = get_db()
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
			user = db.execute(
				'SELECT * FROM user WHERE user.username = ?', (username,)
			).fetchone()
			db.execute(
				'INSERT INTO image (profile_id, image_url, image_type)'
				' VALUES (?, ?, ?)', (user['id'], filename, 'profile')
			)
			db.commit()
			return redirect(url_for('profile.profile', user=user, username=user['username']))

	return render_template('profile/upload_image.html')




@bp.route('/<username>/update_information', methods=('GET', 'POST'))
def update_information(username):
	db = get_db()
	user = db.execute(
		'SELECT * FROM user WHERE user.username = ?', (username,)
	).fetchone()
	if request.method == 'POST':
		last_name = request.form['last_name']
		first_name = request.form['first_name']
		email = request.form['email']
		gender = request.form['gender']
		sexual_pref = request.form['sex_pref']
		bio = request.form['bio']
		tags = request.form['tags']

		db.execute(
			'UPDATE user'
			' SET last_name = ?,'
			' first_name = ?,'
			' email = ?,'
			' gender = ?,'
			' sexual_pref = ?,'
			' biography = ?,'
			' interest_tags = ?'
			' WHERE username = ?',
			(last_name, first_name, email, gender, sexual_pref, bio, tags, username,)
		)
		db.commit()
		
	return render_template('profile/update_information.html', user=user)