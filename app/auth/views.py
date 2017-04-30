from flask import render_template, request, redirect, flash, url_for
from . import auth
from flask_login import login_user
from .forms import LoginForm
from app.models import User


@auth.route('/login')
def login():
    form = LoginForm()

    # todo
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)