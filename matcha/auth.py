
import functools
import datetime

from flask import(
	Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from matcha.db import get_db
from matcha.token import generate_confirmation_token, confirm_token
from matcha.email import send_email

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		email = request.form['email']
		last_name = request.form['last_name']
		first_name = request.form['first_name']
		db = get_db()
		error = None

		if not username:
			error = 'Username is required.'
		elif not password:
			error = 'Password is required.'
		elif not email:
			error = 'Email is required.'
		elif not last_name:
			error = 'Last name is required.'
		elif not first_name:
			error = 'First name is required.'
		elif db.execute(
			'SELECT id FROM user WHERE username = ?', (username,)
		).fetchone() is not None:
			error = 'User {} is already registered.'.format(username)

		if error is None:
			db.execute(
				'INSERT INTO user (username, password, email, last_name, first_name, registered_on, admin, confirmed)'
				' VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
				(username, generate_password_hash(password), email, last_name, first_name, datetime.datetime.now(), False, False)
			)
			db.commit()
			token = generate_confirmation_token(email)
			confirm_url = url_for('auth.confirm_email', token=token, _external=True)
			html = render_template('confirm.html', confirm_url=confirm_url)
			subject = 'Please confirm your email'
			send_email(email, subject, html)
			flash('A confirmation email has been sent via email.', 'success')
			return redirect(url_for('auth.login'))

		flash(error)

	return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		db = get_db()
		error = None
		user = db.execute(
			'SELECT * from user WHERE username = ?', (username,)
		).fetchone()

		if user is None:
			error = 'Incorrect username.'
		elif not check_password_hash(user['password'], password):
			error = 'Incorrect password.'

		if error is None:
			session.clear()
			session['user_id'] = user['id']
			return redirect(url_for('profile.profile', username=user['username'], user=user))

		flash(error)

	return render_template('auth/login.html')


@bp.route('/logout')
def logout():
	session.clear()
	return redirect(url_for('index'))


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * from user WHERE id = ?', (user_id,)
        ).fetchone()


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

@bp.route('/confirm/<token>')
@login_required
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
    user = get_db().execute(
    	'SELECT * FROM user WHERE email = ?', (email,)
    ).fetchone()
    if user['confirmed']:
        flash('Account already confirmed. Please login.', 'success')
    else:
    	db = get_db()
    	db.execute(
    		'UPDATE user'
    		' SET confirmed=True'
    		' WHERE email = ?', (email,)
    	)
        db.commit()
        flash('You have confirmed your account. Thanks!', 'success')
    return render_template('auth/login.html')
