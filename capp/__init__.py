from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os


application = Flask(__name__)

application.config["SECRET_KEY"] = "5791628bb0b13ce0c676dfde280ba245"
# Configure local SQLAlchemy database
application.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///user.db"
application.config["SQLALCHEMY_BINDS"] = {
    "transport": "sqlite:///transport.db",
}

# Create SQLAlchemy instance
db = SQLAlchemy(application)

# set up bcrypt
bcrypt = Bcrypt(application)

# set up a login manager session
login_manager = LoginManager(application)
login_manager.login_view = "user.login"
login_manager.login_message_category = "info"

from capp.home.routes import home
from capp.methodology.routes import methodology
from capp.carbon_app.routes import carbon_app
from capp.aboutUs.routes import aboutUs
from capp.user.routes import user

application.register_blueprint(home)
application.register_blueprint(methodology)
application.register_blueprint(carbon_app)
application.register_blueprint(aboutUs)
application.register_blueprint(user)
