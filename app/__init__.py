from flask import Flask
from app.Controller import errors
from app.Model import models
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_moment import Moment
from flask_bootstrap import Bootstrap
from config import Config



db = SQLAlchemy(app)
Bootstrap = Bootstrap(app)
login = LoginManager(app)
login.login_view = "auth.login"
moment = Moment(app)





from app.Controller import routes, errors
from app.Model import models

def create_app(config_class = Config):

    app = Flask(__name__)
    app.config.from_object(config_class)
    app.static_folder = config_class.STATIC_FOLDER
    app.template_folder = config_class.TEMPLATE_FOLDER

    from app.Controller.errors import errors_blueprint as errors
    app.register_blueprint(errors)
    from app.Controller.auth_routes import auth_blueprint as auth
    app.register_blueprint(auth)
    from app.Controller.routes import routes_blueprint as routes
    app.register_blueprint(auth)
    return app