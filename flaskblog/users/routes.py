from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog import db, bcrypt
from flaskblog.models import User, Post
from flaskblog.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                   RequestResetForm, ResetPasswordForm)
from flaskblog.users.utils import save_picture, send_reset_email

users = Blueprint(name='users', import_name=__name__)


@users.route(rule="/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for(endpoint='main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash(message=f'Your account has been created! You are now able to log in',
              category='success')
        return redirect(url_for(endpoint='users.login'))
    return render_template(template_name_or_list='register.html', title='Register', form=form)


@users.route(rule="/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for(endpoint='main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user=user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(url_for(endpoint='users.account')) if next_page else redirect(url_for(endpoint='main.home'))
        else:
            flash(
                message='Login Unsuccessfull. Please check email and password', category='danger')
    return render_template(template_name_or_list='login.html', title='Login', form=form)


@users.route(rule="/logout")
def logout():
    logout_user()
    return redirect(url_for(endpoint='main.home'))


@users.route(rule="/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        db.session.commit()
        flash(message='Your account has been updated!', category='success')
        return redirect(url_for(endpoint='users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for(
        endpoint='static', filename=f'profile_pics/{current_user.image_file}')
    return render_template(template_name_or_list='account.html', title='Account', image_file=image_file, form=form)


@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get(key='page', default=1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(
        Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template(template_name_or_list="user_posts.html", posts=posts, user=user)


@users.route(rule="/reset_password", methods=["GET", "POST"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for(endpoint='main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user=user)
        flash(message='An email has been sent with instructions to reset your password.', category='info')
        return redirect(location=url_for(endpoint='users.login'))
    return render_template(template_name_or_list='reset_request.html', title='Reset Password', form=form)


@users.route(rule="/reset_password/<string:token>", methods=["GET", "POST"])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for(endpoint='main.home'))
    user = User.verify_reset_token(token=token)

    if user is None:
        flash(message='That is an invalid or expired token.', category='warning')
        return redirect(location=url_for(endpoint='users.reset_request'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user.password = hashed_pw
        db.session.commit()
        flash(message=f'Your password has been updated! You are now able to log in',
              category='success')
        return redirect(url_for(endpoint='users.login'))
    return render_template(template_name_or_list='reset_token.html', title='Reset Password', form=form)
