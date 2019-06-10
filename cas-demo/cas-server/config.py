# encoding: utf-8
import os


# 为了使用session，而加盐
SECRET_KEY = os.urandom(24)

# 连接数据库的配置
HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'cas_server'
USERNAME = 'root'
PASSWORD = ''

# 标准格式：dialect+driver://username:password@host:port/database
DB_URI = 'mysql+mysqldb://%s:%s@%s:%s/%s?charset=utf8' % \
         (USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI

SQLALCHEMY_TRACK_MODIFICATION = False


