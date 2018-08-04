
from flask import current_app
from flask_mail import Mail, Message




def send_email(to, subject, template):
	mail = Mail()
	mail.init_app(current_app)
	msg = Message(
		subject,
		recipients=[to],
		html=template,
		sender=current_app.config['MAIL_DEFAULT_SENDER']
	)
	mail.send(msg)