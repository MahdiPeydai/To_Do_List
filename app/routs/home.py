from flask import render_template, Blueprint

home = Blueprint('home', __name__,
                 template_folder='templates',
                 static_folder='static'
                 )


@home.route('/')
@home.route('/home')
@home.route('/index')
def index():
    return render_template('home/index.html')
