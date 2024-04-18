from capp import db
from capp import application
from capp.models import User, Transport
from datetime import datetime, timedelta

db.create_all(app=application)
