from wtforms import Form, StringField, PasswordField, DateField, FileField, TimeField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from flask_wtf.file import FileSize, FileAllowed, FileRequired
from To_Do_List import app


class LoginForm(Form):
    email = StringField('Email',
                        validators=[DataRequired(),
                                    Email(),
                                    Length(max=120)],
                        render_kw={"placeholder": "Email"})
    password = PasswordField('Password',
                             validators=[DataRequired()])


class RegisterForm(Form):
    name = StringField('Username',
                       validators=[DataRequired(),
                                   Length(max=16)],
                       render_kw={"placeholder": "Name"})
    email = StringField('Email',
                        validators=[DataRequired(),
                                    Email(),
                                    Length(max=120)],
                        render_kw={"placeholder": "Email"})
    phone = StringField('Phone Number',
                        validators=[DataRequired(),
                                    Length(min=11, max=11, message='Correct Format : "09** *** ****"')],
                        render_kw={"placeholder": "09** *** ****"})
    password = PasswordField('Password',
                             validators=[DataRequired(),
                                         Length(min=8, message='Password should be at least %(min)d characters long')])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(),
                                                 EqualTo('password', message='Passwords must match!')])


class CreateCategoryForm(Form):
    category_name = StringField('Username',
                                validators=[DataRequired(),
                                            Length(max=16)],
                                render_kw={"placeholder": "Category Name"})


class CreateActivityForm(Form):
    activity_name = StringField('Activity Name',
                                validators=[DataRequired(),
                                            Length(max=16)],
                                render_kw={"placeholder": "Activity Name"})
    activity_exp_date = DateField('Expiration date',
                                  validators=[DataRequired()])
    activity_exp_time = TimeField('Expiration time',
                                  validators=[DataRequired()])
    activity_avatar = FileField('Avatar',
                                validators=[FileSize(max_size=1),
                                            FileAllowed(app.config['ACTIVITY_AVATAR_ALLOWED_EXTENSIONS'])])


class Information(Form):
    user_name = StringField('Username',
                            validators=[DataRequired(),
                                        Length(max=16)],
                            render_kw={"placeholder": 'New Username'})
    user_email = StringField('Email',
                             validators=[DataRequired(),
                                         Email(),
                                         Length(max=120)],
                             render_kw={"placeholder": "New Email"})
    user_phone = StringField('Phone Number',
                             validators=[DataRequired(),
                                         Length(min=11, max=11, message='Correct Format : "09** *** ****"')],
                             render_kw={"placeholder": "New Phone Number"})


class ChangePassword(Form):
    old_password = PasswordField('Old Password',
                                 validators=[DataRequired(),
                                             Length(min=8,
                                                    message='Password should be at least %(min)d characters long')])
    password = PasswordField('New Password',
                             validators=[DataRequired(),
                                         Length(min=8, message='Password should be at least %(min)d characters long')])
    confirm_password = PasswordField('Confirm New Password',
                                     validators=[DataRequired(),
                                                 EqualTo('password', message='Passwords must match!')])
