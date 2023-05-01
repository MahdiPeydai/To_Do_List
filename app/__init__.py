from flask import Flask


app = Flask(__name__)
app.config.from_pyfile('../config.py')

from .routs.home import home
from .routs.auth import auth
from .routs.dashboard import dashboard
from .routs.profile import profile

app.register_blueprint(home)
app.register_blueprint(auth)
app.register_blueprint(profile)
app.register_blueprint(dashboard)
