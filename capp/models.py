from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from capp import db, login_manager
from flask_login import UserMixin
from datetime import datetime


class User(db.Model, UserMixin):
    __tablename__ = "user_table"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    transport = db.relationship("Transport", backref="author", lazy=True)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Transport(db.Model):
    __bind_key__ = "transport"
    __tablename__ = "transport_table"
    id = db.Column(db.Integer, primary_key=True)
    kms = db.Column(db.Float)
    transport = db.Column(db.String)
    fuel = db.Column(db.String)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now())
    co2 = db.Column(db.Float)
    total = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey("user_table.id"), nullable=False)

    def __repr__(self):
        return f"Transport('{self.kms}', '{self.transport}', '{self.fuel}', '{self.date}', '{self.co2}', '{self.total}', '{self.user_id}')"
