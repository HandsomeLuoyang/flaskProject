# coding: utf-8
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash


db = SQLAlchemy()


class UserPowerTable(db.Model):
    __tablename__ = 'user_power_table'

    pow_id = db.Column(db.Integer, primary_key=True)
    pow_name = db.Column(db.String(50), nullable=False)


class UserTable(db.Model, UserMixin):
    __tablename__ = 'user_table'

    user_id = db.Column(db.Integer, primary_key=True)
    pow_id = db.Column(
        db.ForeignKey(
            'user_power_table.pow_id',
            ondelete='RESTRICT',
            onupdate='RESTRICT'),
        nullable=False,
        index=True)
    user_name = db.Column(db.String(50), nullable=False)
    user_password = db.Column(db.String(18), nullable=False)

    pow = db.relationship(
        'UserPowerTable',
        primaryjoin='UserTable.pow_id == UserPowerTable.pow_id',
        backref='user_tables')

    def __init__(self, user_id, pow_id, user_name, user_password):
        self.user_id = user_id
        self.pow_id = pow_id
        self.user_name = user_name
        self.user_password = generate_password_hash(user_password)

    def get_id(self):
        return self.user_id

    def verify_password(self, password):
        return check_password_hash(self.user_password, password)

