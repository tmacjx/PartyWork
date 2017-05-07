from flask import Blueprint

main = Blueprint('main', __name__)


from .import views, errors
from app.decorators import admin_required, permission_required
from flask_login import login_required
from flask import send_from_directory
# from flask import app
# todo 负责登陆 等通用基础功能
import app


@main.route('/admin')
@login_required
@admin_required
def for_admin_only():
    return 'For Administrators!'


@main.route('/media/<filename>')
def media(filename):
    return send_from_directory(app.config.MEDIA_PATH,
                               filename)


