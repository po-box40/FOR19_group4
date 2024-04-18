from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os


application = Flask(__name__)

# Configring for AWS, secret key and database
# application.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

# secret key for the database
application.config["SECRET_KEY"] = "A@RrwCo@4A@Kow@8J&z8c8hvmN28"


""" DBVAR = f"postgresql://{os.environ.get('RDS_USERNAME')}:{os.environ.get('RDS_PASSWORD')}@{os.environ.get('RDS_HOSTNAME')}/{os.environ.get('RDS_DB_NAME')}"
application.config["SQLALCHEMY_DATABASE_URI"] = DBVAR
application.config["SQLALCHEMY_BINDS"] = {
    "transport": DBVAR,
}
application.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False """

# set up local database
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
