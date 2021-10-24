from flask_login import LoginManager

from config import Config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login = LoginManager(app)
login.login_view = 'login'


from app import routes, models


# 访问 https://www.jetbrains.com/help/pycharm/ 获取 PyCharm 帮助
