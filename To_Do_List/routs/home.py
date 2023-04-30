from flask import render_template, redirect, request, Blueprint, url_for, flash
from To_Do_List import app
from To_Do_List.helpers.token_check import token_check
from To_Do_List.helpers.get_username_by_id import get_username
from To_Do_List.helpers.forms import CreateCategoryForm
from To_Do_List.helpers.forms import CreateActivityForm
import os
import json


home = Blueprint('home', __name__,
                 template_folder='templates',
                 static_folder='static'
                 )


@home.route('/home')
@token_check
def home_page(user_id):
    user_name = get_username(user_id)

    with open('To_Do_List/data/users_categories.json', 'r') as categories_file:
        categories = json.load(categories_file)

    with open('To_Do_List/data/users_activities.json', 'r') as activities_file:
        activities = json.load(activities_file)

    user_activities = {}
    user_categories = {}
    for user_category_check in categories:
        if user_category_check['user_id'] == user_id:
            user_categories['{}'.format(user_category_check['category_id'])] = user_category_check['category_title']
            category_activities = []
            for user_activity_check in activities:
                if user_activity_check['category_id'] == user_category_check['category_id']:
                    activity = {
                        "activity_id": user_activity_check["activity_id"],
                        "activity_name": user_activity_check["activity_name"],
                        "activity_date": user_activity_check["activity_date"],
                        "activity_time": user_activity_check["activity_time"],
                        "activity_status": user_activity_check["activity_status"],
                        "activity_avatar": user_activity_check["activity_avatar"]
                    }
                    category_activities.append(activity)
            user_activities['{}'.format(user_category_check['category_id'])] = category_activities
    return render_template('home/home.html', user_name=user_name, user_categories=user_categories, user_activities=user_activities)


@home.route('/user/category/<int:category_id>/activity/<int:activity_id>/status')
@token_check
def status_changer(user_id, category_id, activity_id):
    with open('To_Do_List/data/users_activities.json', 'r+') as activities_file:
        activities = json.load(activities_file)
    for activity_check in activities:
        if user_id == activity_check['user_id'] and\
                category_id == activity_check['category_id'] and\
                activity_id == activity_check['activity_id']:
            if activities[activities.index(activity_check)]['activity_status'] == 'not done':
                activities[activities.index(activity_check)]['activity_status'] = 'done'
            else:
                activities[activities.index(activity_check)]['activity_status'] = 'not done'

    with open('To_Do_List/data/users_activities.json', 'w+') as activities_file:
        json.dump(activities, activities_file, indent=2)

    return redirect(url_for('home.home_page'))


@home.route('/user/category/<int:category_id>/activity/<int:activity_id>/delete')
@token_check
def delete_activity(user_id, category_id, activity_id):
    with open('To_Do_List/data/users_activities.json', 'r+') as activities_file:
        activities = json.load(activities_file)
    for activity_check in activities:
        if user_id == activity_check['user_id'] and\
                category_id == activity_check['category_id'] and\
                activity_id == activity_check['activity_id']:
            del activities[activities.index(activity_check)]
            with open('To_Do_List/data/users_activities.json', 'w+') as activities_file:
                json.dump(activities, activities_file, indent=2)
            os.remove(os.path.join(app.config['ACTIVITY_AVATAR_UPLOAD_FOLDER'], 'activity_{}.png'.format(activity_check['activity_id'])))
    return redirect(url_for('home.home_page'))


@home.route('/user/category/<int:category_id>/delete')
@token_check
def delete_category(user_id, category_id):
    with open('To_Do_List/data/users_categories.json', 'r+') as categories_file:
        categories = json.load(categories_file)
    for category_check in categories:
        if category_check['user_id'] == user_id and category_check['category_id'] == int(category_id):
            del categories[categories.index(category_check)]
            with open('To_Do_List/data/users_categories.json', 'w+') as categories_file:
                json.dump(categories, categories_file, indent=2)
            return redirect(url_for('home.home_page'))


@home.route('/user/category/<int:category_id>/activity/create', methods=['POST', 'GET'])
@token_check
def create_activity(user_id, category_id):
    user_name = get_username(user_id)
    form = CreateActivityForm(request.form)
    if request.method == 'POST' and form.validate():
        with open('To_Do_List/data/users_activities.json', 'r+') as activity_files:
            activities = json.load(activity_files)

        for activity_check in activities:
            if request.form['activity_name'].strip() == activity_check['activity_name'] and \
                    activity_check['user_id'] == user_id and \
                    activity_check['category_id'] == category_id:
                flash('Activity already exist')
                return redirect(url_for('home.create_activity', category_id=category_id))

        new_activity_id = activities[-1]['activity_id'] + 1

        new_activity_avatar = request.files['activity_avatar']
        new_activity_avatar_filename = 'activity_{}.png'.format(new_activity_id)
        new_activity_avatar.save(os.path.join(app.config["ACTIVITY_AVATAR_UPLOAD_FOLDER"], new_activity_avatar_filename))

        new_activity = {
            "user_id": user_id,
            "category_id": category_id,
            "activity_id": new_activity_id,
            "activity_name": request.form['activity_name'],
            "activity_date": request.form['activity_exp_date'],
            "activity_time": request.form['activity_exp_time'],
            "activity_status": 'not done',
            "activity_avatar": new_activity_avatar_filename
        }

        activities.append(new_activity)
        with open('To_Do_List/data/users_activities.json', 'w') as activities_file:
            json.dump(activities, activities_file, indent=2)

        return redirect(url_for('home.home_page'))
    return render_template('home/create_activity_page.html', user_name=user_name, form=form)


@home.route('/user/category/create', methods=['POST', 'GET'])
@token_check
def create_category(user_id):
    user_name = get_username(user_id)
    form = CreateCategoryForm(request.form)
    if request.method == 'POST' and form.validate():
        with open('To_Do_List/data/users_categories.json', 'r+') as categories_file:
            categories = json.load(categories_file)
        for category_check in categories:
            if category_check['user_id'] == user_id and request.form['category_name'].strip() == category_check['category_title']:
                flash('Category already exist')
                return redirect(url_for('home.create_category'))
        new_category_title = request.form['category_name'].strip()
        new_category_id = categories[-1]['category_id'] + 1
        new_category = {
            "user_id": user_id,
            "category_title": new_category_title,
            "category_id": new_category_id
        }
        categories.append(new_category)
        with open('To_Do_List/data/users_categories.json', 'w+') as categories_file:
            json.dump(categories, categories_file, indent=2)
        return redirect(url_for('home.home_page'))
    return render_template('home/create_category_page.html', user_name=user_name, form=form)
