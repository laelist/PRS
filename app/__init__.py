from config import Config

import os
import logging
from logging.handlers import RotatingFileHandler
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_moment import Moment

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login = LoginManager(app)
login.login_view = 'login'

bootstrap = Bootstrap(app)

moment = Moment(app)


if not app.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/PRS.log', maxBytes=10240,
                                       backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('PRS startup')


from app import routes, models, errors


# 访问 https://www.jetbrains.com/help/pycharm/ 获取 PyCharm 帮助
