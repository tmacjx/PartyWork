from flask_admin.contrib.sqla import ModelView
from wtforms.validators import DataRequired
from flask_login import current_user
from flask import redirect, url_for, request
from wtforms.fields import PasswordField
from flask_admin import form
from app import config
from jinja2 import Markup
from flask_pagedown.fields import PageDownField


MEDIA_PATH = config.MEDIA_PATH


class AdminView(ModelView):

    def is_accessible(self):
        return current_user.is_administrator

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('auth.login', next=request.url))


class RoleView(AdminView):
    can_delete = False
    column_editable_list = ['name', 'users']
    form_excluded_columns = ['users']
    form_args = {
        'name': {
            'label': '角色名称',
            'validators': [DataRequired()]
        }
    }


class UserView(AdminView):
    form_excluded_columns = ['password_hash']
    form_args = {
        'username': {
            'label': '用户名',
            'validators': [DataRequired()]
        },
        'email': {
            'label': '邮箱',
            'validators': [DataRequired()]
        },
        'role': {
            'label': '身份',
            'validators': [DataRequired()]
        }
    }
    column_exclude_list = ['password', 'password_hash']

    def scaffold_form(self):
        # Start with the standard form as provided by Flask-Admin. We've already told Flask-Admin to exclude the
        # password field from this form.
        form = super(UserView, self).scaffold_form()

        # Add a password field, naming it "password2" and labeling it "New Password".
        form.password = PasswordField(label='密码')
        return form


# todo 文件名uuid？？
class FileView(AdminView):
    # Override form field to use Flask-Admin FileUploadField
    form_overrides = {
        'img_path': form.FileUploadField
    }

    # Pass additional parameters to 'path' to FileUploadField constructor
    form_args = {
        'img_path': {
            'label': 'File',
            'base_path': MEDIA_PATH,
            'allow_overwrite': False
        }
    }
    form_excluded_columns = ['content_html']


# todo 编辑页面 图片路径 显示错误？？
class ImageView(AdminView):

    def _list_thumbnail(view, context, model, name):
        if not model.img_path:
            return ''

        return Markup('<img src="%s">' % url_for('main.media',
                                                 filename=model.img_path))
    column_formatters = {
        'img_path': _list_thumbnail
    }

    # Alternative way to contribute field is to override it completely.
    # In this case, Flask-Admin won't attempt to merge various parameters for the field.
    form_extra_fields = {
        'img_path': form.ImageUploadField('Image', base_path=MEDIA_PATH),
        'content': PageDownField(validators=[DataRequired()])
    }

    form_excluded_columns = ['content_html']






