from flask import Flask


app = Flask(__name__)
app.config.from_pyfile('../config.py')

from .routs.blog import blog
from .routs.auth import auth
from .routs.home import home
from .routs.profile import profile

app.register_blueprint(home)
app.register_blueprint(auth)
app.register_blueprint(profile)
app.register_blueprint(blog)
