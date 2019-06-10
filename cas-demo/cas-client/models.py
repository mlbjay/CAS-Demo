# encoding: utf-8
import time
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Info(db.Model):
    """
    信息表：用户名，信息
    """
    __tablename__ = 'information'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(32), nullable=False)
    info = db.Column(db.String(100), nullable=False)


class ST(db.Model):
    """
    service_ticket表：service_ticket，是否有效(-1：无效，1：有效)
    """
    __tablename__ = 'service_ticket'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    st = db.Column(db.String(100), nullable=False)
    validate = db.Column(db.Integer, nullable=False, default=1)




