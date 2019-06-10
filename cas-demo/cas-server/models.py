# encoding: utf-8
import time
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model):
    """
    用户表：用户名，密码
    """
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(32), nullable=False)
    password = db.Column(db.String(32), nullable=False)
    info = db.Column(db.String(100), nullable=False)


class Service(db.Model):
    """
    服务接入表：url
    """
    __tablename__ = 'service'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String(100), nullable=False)
    logout_url = db.Column(db.String(100), nullable=False)


class TGT(db.Model):
    """
    TGT表：大令牌，user.id，过期时间，是否有效(-1：无效，1：有效)
    """
    __tablename__ = 'ticket_granted_ticket'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tgt = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    expires_in = db.Column(db.BigInteger, nullable=True)
    validate = db.Column(db.Integer, nullable=False, default=1)


class ST(db.Model):
    """
    ST表：小令牌，User.id，TGT.id，Service.id，使用次数，过期时间，是否有效(-1：无效，1：有效)
    """
    __tablename__ = 'service_ticket'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    st = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    tgt_id = db.Column(db.Integer, nullable=False)
    service_id = db.Column(db.Integer, nullable=False)
    url = db.Column(db.String(100), nullable=False)
    used = db.Column(db.Integer, nullable=False)
    expires_in = db.Column(db.BigInteger, nullable=True)
    validate = db.Column(db.Integer, nullable=False, default=1)






