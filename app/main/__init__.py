from flask import Blueprint

main = Blueprint('main', __name__)


from .import views, errors
from app.decorators import admin_required, permission_required
from flask_login import login_required


# todo 负责登陆 等通用基础功能

@main.route('/admin')
@login_required
@admin_required
def for_admin_only():
    return 'For Administrators!'


