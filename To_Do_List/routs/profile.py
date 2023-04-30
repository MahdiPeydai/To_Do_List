from flask import render_template, redirect, request, Blueprint, url_for, flash
from To_Do_List.helpers.token_check import token_check
from To_Do_List.helpers.forms import Information
from To_Do_List.helpers.forms import ChangePassword

import json
import hashlib


profile = Blueprint('profile', __name__,
                    template_folder='templates',
                    static_folder='static'
                    )


@profile.route('/user/information', methods=['POST', 'GET'])
@token_check
def information(user_id):
    with open('../To_Do_List/To_Do_List/data/users_information.json', 'r+') as information_file:
        users_information = json.load(information_file)
    for account_check in users_information:
        if account_check['user_id'] == user_id:
            user_info = account_check
    placeholders = {
        'user_name': user_info['user_name'],
        'user_email': user_info['user_email'],
        'user_phone': user_info['user_phone']
    }
    form = Information(request.form, data=placeholders)
    return render_template('profile/account_information_page.html', user_info=user_info, form=form)


@profile.route('/user/information/edit/<edited_information>', methods=['POST', 'GET'])
@token_check
def edit_information(user_id, edited_information):
    if request.method == 'POST':
        with open('../To_Do_List/To_Do_List/data/users_information.json', 'r+') as information_file:
            users_information = json.load(information_file)
        for user_check in users_information:
            if user_check['user_id'] == user_id:
                users_information[users_information.index(user_check)][edited_information] = request.form[edited_information]
                with open('../To_Do_List/To_Do_List/data/users_information.json', 'w+') as information_file:
                    json.dump(users_information, information_file, indent=2)
                flash('Successfully changed')
                return redirect(url_for('profile.information'))


@profile.route('/user/delete')
@token_check
def delete_account(user_id):
    with open('../To_Do_List/To_Do_List/data/users_information.json', 'r+') as information_file:
        users_information = json.load(information_file)
    for user_check in users_information:
        if user_check['user_id'] == user_id:
            del users_information[users_information.index(user_check)]
            with open('../To_Do_List/To_Do_List/data/users_information.json', 'w+') as information_file:
                json.dump(information, information_file, indent=2)
            flash('Account deleted successfully')
            return redirect(url_for('auth.login'))


@profile.route('/user/information/password/edit', methods=['POST', 'GET'])
@token_check
def change_password(user_id):
    form = ChangePassword(request.form)
    if request.method == 'POST' and form.validate():
        with open('../To_Do_List/To_Do_List/data/users_information.json', 'r+') as information_file:
            users_information = json.load(information_file)
        for user_check in users_information:
            if user_check['user_id'] == user_id:
                user = user_check
                break
        user_old_password = request.form['old_password']
        user_old_password = user_old_password.encode()
        user_hashed_old_password = (hashlib.sha256(user_old_password)).hexdigest()
        if user_hashed_old_password != user['user_password']:
            flash('Wrong password')
            return redirect(url_for('profile.change_password'))
        user_new_password = request.form['password']
        user_new_password = user_new_password.encode()
        user_hashed_new_password = (hashlib.sha256(user_new_password)).hexdigest()
        users_information[users_information.index(user)]['user_password'] = user_hashed_new_password
        with open('../To_Do_List/To_Do_List/data/users_information.json', 'w+') as information_file:
            json.dump(users_information, information_file, indent=2)
        flash('Password successfully changed')
        return redirect(url_for('profile.information'))
    return render_template('profile/password_change_page.html', form=form)
