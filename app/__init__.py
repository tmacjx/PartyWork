from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_login import LoginManager
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from app.admin.views import RoleView, UserView
# from flask_mail import Mail
import os


bootstrap = Bootstrap()
db = SQLAlchemy()
# mail = Mail()

admin = Admin(name='admin')

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

app = Flask(__name__)

config_name = os.environ['MODE']

app.config.from_object(config[config_name])


def create_app():
    from .models import Role, User

    # app = Flask(__name__)

    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    admin.init_app(app)
    # mail.init_app(app)

    admin.add_view(RoleView(Role, db.session))
    admin.add_view(UserView(User, db.session))

    from .main import main as main_blueprint

    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint

    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app

