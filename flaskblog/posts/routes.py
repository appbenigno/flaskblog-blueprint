from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Post
from flaskblog.posts.forms import PostForm
import json

posts = Blueprint(name='posts', import_name=__name__)


@posts.route(rule="/generate")
def generate():
    file = open(file="flaskblog/posts.json", mode="r")
    data = json.load(file)

    for element in data:
        post = Post(title=element.get('title'), content=element.get(
            'content'), user_id=element.get('user_id'))
        db.session.add(post)

    db.session.commit()

    flash(message='Posts Generated!', category='success')
    return redirect(location=url_for(endpoint='main.home'))


@posts.route(rule="/post/new", methods=["GET", "POST"])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data,
                    content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash(message='Your post has been created', category='success')
        return redirect(location=url_for(endpoint='main.home'))
    return render_template(template_name_or_list='create_post.html', title='New Post', form=form, legend='New post')


@posts.route(rule="/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template(template_name_or_list='post.html', title=post.title, post=post)


@posts.route(rule="/post/<int:post_id>/update", methods=["GET", "POST"])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash(message='Your post has been updated!', category='success')
        return redirect(location=url_for(endpoint='posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template(template_name_or_list='create_post.html', title='Update Post', form=form, legend='Update Post')


@posts.route(rule="/post/<int:post_id>/delete", methods=["GET", "POST"])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash(message='Your post has been deleted!', category='success')
    return redirect(location=url_for(endpoint='main.home'))
