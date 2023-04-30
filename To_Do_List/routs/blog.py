from flask import render_template, Blueprint, flash

blog = Blueprint('blog', __name__,
                 template_folder='templates',
                 static_folder='static'
                 )


@blog.route('/')
@blog.route('/index')
def index():
    return render_template('blog/index.html')
