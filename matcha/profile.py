
import functools

from flask import(
	Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from matcha.db import get_db

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
	
	flash(error)
	return render_template('profile/profile.html', user=user)


