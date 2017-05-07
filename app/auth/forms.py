from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Length, Email, DataRequired, Regexp, EqualTo, ValidationError

from ..models import User


class LoginForm(Form):
    email = StringField('邮箱', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('密码', validators=[DataRequired()])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登陆')


class RegistrationForm(Form):
    email = StringField('邮箱', validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField('用户名', validators=[DataRequired(), Length(1, 64),
                                                   Regexp('^[A-Za-z0-9_.]*$', 0,
                                                          'Username must have only letters, numbers, '
                                                          'dots or underscores')])
    password = PasswordField('密码', validators=[DataRequired(), EqualTo('password2', message='Password must match')])
    password2 = PasswordField('确认密码', validators=[DataRequired()])

    submit = SubmitField('注册')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('该邮箱已注册')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已存在')


class ChangePasswordForm(Form):
    old_password = PasswordField('旧密码', validators=[DataRequired()])
    password = PasswordField('新密码', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('确认新密码', validators=[DataRequired()])
    submit = SubmitField('提交')


class EditProfileForm(Form):
    name = StringField('真名', validators=[Length(0, 64)])
    about_me = StringField('关于我')
    submit = SubmitField('提交')
