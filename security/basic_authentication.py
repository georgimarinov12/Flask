from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

from errors import ApplicationError
from errors import register_error_handlers
from model.user import User


def get_password_hash(password):
    return generate_password_hash(password)


def verify_password(email, password):
    user = None
    try:
        user = User.find_by_email(email)
    except ApplicationError as err:
        if err.status_code != 404:
            raise err

    return user is not None and check_password_hash(user.password, password)


#def init_basic_auth():
#    auth = HTTPBasicAuth()
#    auth.verify_password(__verify_password)
#    return auth
    
def require_login(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.cookies.get('token')
        if not token or not User.verify_token(token):
            return "Unauthorized", 401
        return func(*args, **kwargs)
    return wrapper
