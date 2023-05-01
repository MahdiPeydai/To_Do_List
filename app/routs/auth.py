from flask import render_template, redirect, request, make_response, Blueprint, url_for, flash
from app import app
from app.helpers.forms import RegisterForm
from app.helpers.forms import LoginForm
import hashlib
import json
import jwt

auth = Blueprint('auth', __name__,
                 template_folder='templates',
                 static_folder='static'
                 )


@auth.route('/auth/login', methods=['POST', 'GET'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST':
        user_email = request.form['email']
        user_password = request.form['password']
        user_password = user_password.encode()
        user_password = (hashlib.sha256(user_password)).hexdigest()

        with open('app/data/users_information.json', 'r+') as information_file:
            information = json.load(information_file)

        for user_check in information:
            if (user_check['user_email'] == user_email) and (user_check['user_password'] == user_password):
                user_id = user_check['user_id']
                resp = make_response(redirect(url_for('dashboard.dashboard_page')))
                token = jwt.encode({'user_id': user_id}, app.config['SECRET_KEY'], 'HS256')
                resp.set_cookie('token', token)
                return resp
        flash('Wrong username or password. Please try again ...')
        return redirect(url_for('auth.login'))

    return render_template('auth/login_page.html', form=form)


@auth.route('/auth/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        user_email = request.form['email']

        with open('app/data/users_information.json', 'r+') as information_file:
            information = json.load(information_file)

        for user_email_check in information:
            if user_email_check['user_email'] == user_email:
                flash('An account already exists with this email address', 'error_type')
                return redirect(url_for('auth.register'))

        user_password = request.form['password']
        user_password = user_password.encode()
        user_hashed_password = (hashlib.sha256(user_password)).hexdigest()

        user_name = request.form['name']
        user_phone = request.form['phone']

        if len(information) != 0:
            user_id = information[-1]['user_id'] + 1
        else:
            user_id = 1

        new_user_information = {
            'user_id': user_id,
            'user_email': user_email,
            'user_name': user_name,
            'user_phone': user_phone,
            'user_password': user_hashed_password
        }
        information.append(new_user_information)
        with open("app/data/users_information.json", 'w+') as information_file:
            json.dump(information, information_file, indent=2)

        resp = make_response(redirect(url_for('dashboard.home_page')))
        token = jwt.encode({'user_id': user_id}, app.config['SECRET_KEY'], 'HS256')
        resp.set_cookie('token', token)
        return resp
    return render_template('auth/register_page.html', form=form)


@auth.route('/auth/logout')
def logout():
    resp = make_response(redirect(url_for('auth.login')))
    resp.set_cookie('token', '', expires=0)
    return resp
