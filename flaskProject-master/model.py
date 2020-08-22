# coding: utf-8
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class UserPowerTable(db.Model):
    __tablename__ = 'user_power_table'

    pow_id = db.Column(db.Integer, primary_key=True)
    pow_name = db.Column(db.String(50), nullable=False)


class UserTable(db.Model):
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
