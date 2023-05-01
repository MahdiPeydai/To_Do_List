from flask import request, redirect, url_for, flash
from app import app
import jwt
from functools import wraps


def token_check(func):
    @wraps(func)
    def decorator(*args, **kwargs):

        if 'token' in request.cookies:
            token = request.cookies.get('token')
        else:
            flash('Login Required', 'error_type')
            return redirect(url_for('auth.login'))

        try:
            current_user_id = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user_id = current_user_id['user_id']
        except:
            flash('Login Required')
            return redirect(url_for('auth.login'))
        else:
            return func(current_user_id, *args, **kwargs)
    return decorator
