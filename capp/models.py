from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from capp import db, login_manager
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = "user_table"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    transport_id = db.Column(db.Integer, ForeignKey("transport_table.id"))
    transport = db.relationship("Transport", back_populates="users")


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Transport(db.Model):
    __bind_key__ = "transport"
    __tablename__ = "transport_table"

    id = db.Column(db.Integer, primary_key=True)
    # Add more attributes specific to the Transport class if needed
    user_id = db.Column(db.Integer, ForeignKey("user_table.id"), nullable=False)
