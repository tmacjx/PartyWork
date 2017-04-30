from flask import Blueprint

main = Blueprint('main', __name__)


from .import views, errors

# todo 负责登陆 等通用基础功能