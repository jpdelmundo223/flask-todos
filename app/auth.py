from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, current_user, login_required
from .models import Users
from .forms import LoginForm, SignUpForm
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

auth = Blueprint("auth", __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    title = 'Login'
    form = LoginForm()
    if request.method == "POST":
        if form.validate_on_submit():
            user = Users.query.filter_by(username=form.username.data).first()
            if user:
                if check_password_hash(user.password, form.password.data):
                    login_user(user, remember=form.remember_me.data)
                    return redirect(url_for('todo.index'))
                else:
                    flash("Incorrect username or password!", "danger")
            else:
                flash("User does not exists!", "danger")
    return render_template('auth/login.html', title=title,
                                                form=form)

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    title = 'Sign-Up'
    form = SignUpForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            username = Users.query.filter_by(username=form.username.data).first()
            if username is None:
                new_user = Users(first_name=form.first_name.data, 
                                    last_name=form.last_name.data,
                                    username=form.username.data,
                                    password=generate_password_hash(form.password.data))
                db.session.add(new_user)
                db.session.commit()
                flash("You have been successfully signed up!", "success")
            else:
                flash("Username already exists!", "danger")
    return render_template('auth/register.html', title=title,
                                                    form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))