import os

DEBUG = True
basedir = os.path.abspath(os.path.dirname(__file__))
DIALECT = 'mysql'
DRIVER = 'pymysql'
USERNAME = 'chao'
PASSWORD = '235711'
HOST = '127.0.0.1'
PORT = '3306'
DATABASE = 'prs'
DB_URL = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(
    DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT, DATABASE)


class Config(object):
    # SECRET_KEY = os.urandom(24)
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or DB_URL
    # 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    PROJECT_PER_PAGE = 3

    MAX_CONTENT_LENGTH = 50 * 1024 * 1024

