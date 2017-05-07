from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from config import load_config
from flask_login import LoginManager
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
# from app.admin.views import RoleView, UserView, ImageView
# from flask_mail import Mail
import os
from flask_pagedown import PageDown
from flask.ext.moment import Moment

bootstrap = Bootstrap()
db = SQLAlchemy()
# mail = Mail()

f_admin = Admin(name='admin')
moment = Moment()


pageDown = PageDown()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

app = Flask(__name__, static_folder='static')


config = load_config()

app.config.from_object(config)


def create_app():

    from .models import Role, User, CurrentNews, WorkTrends, Activity, PartyMember, LearnContent
    # import app.admin.views as app_Admin
    from app.admin.views import RoleView, UserView, ImageView

    # app = Flask(__name__)
    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    f_admin.init_app(app)
    pageDown.init_app(app)
    moment.init_app(app)

    # mail.init_app(app)

    f_admin.add_view(RoleView(Role, db.session))
    f_admin.add_view(UserView(User, db.session))
    f_admin.add_view(ImageView(CurrentNews, db.session))
    f_admin.add_view(ImageView(WorkTrends, db.session))
    f_admin.add_view(ImageView(Activity, db.session))
    f_admin.add_view(ImageView(PartyMember, db.session))

    from .main import main as main_blueprint

    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint

    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app

