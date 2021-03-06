from flask import render_template, request, redirect, flash, url_for
from . import auth
from flask_login import login_user, logout_user
from .forms import LoginForm, RegistrationForm, ChangePasswordForm, EditProfileForm
from app.models import User
from flask_login import current_user, login_required
from app import db


@auth.before_app_request
def before_request():
    """
    记录最近登陆时间
    :return:
    """
    if current_user.is_authenticated:
        current_user.ping()
        # if not current_user.confirmed and request.endpoint[:5] != 'auth.':
        #     return redirect(url_for('auth.unconfirmed'))


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        # todo 发送确认邮件 重设邮箱 忘记密码 修改密码
        flash('You can now login')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            flash('Your password has been updated.')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid password.')
    return render_template("auth/change_password.html", form=form)


@auth.route('/edit-profile', methods=['GET', 'POST'])
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash('Your profile has been updated')
        return redirect(url_for('main.user', username=current_user.username))
    form.name.data = current_user.name
    form.about_me.data = current_user.about_me
    return render_template('edit-profile.html', form=form)



