

from itsdangerous import URLSafeTimedSerializer

from matcha import matcha


def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(matcha.config['SECRET_KEY'])
    return serializer.dumps(email, salt=matcha.config['SECURITY_PASSWORD_SALT'])


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(matcha.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=matcha.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration
        )
    except:
        return False
    return email