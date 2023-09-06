from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_moment import Moment
from flask_bootstrap import Bootstrap


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
Bootstrap = Bootstrap(app)

login = LoginManager(app)
login.login_view = "login"

moment = Moment(app)


from app import routes, models, errors
