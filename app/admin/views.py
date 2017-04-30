from flask_admin.contrib.sqla import ModelView
from wtforms.validators import DataRequired
from flask_login import current_user
from flask import redirect, url_for, request
from wtforms.fields import PasswordField


class AdminView(ModelView):

    def is_accessible(self):
        # todo 必须是管理员身份，如何通过cmd生成一个 管理员？？
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

