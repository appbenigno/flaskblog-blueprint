from flask import render_template, request, Blueprint
from flaskblog.models import Post

main = Blueprint(name='main', import_name=__name__)


@main.route("/")
@main.route("/home")
def home():
    page = request.args.get(key='page', default=1, type=int)
    posts = Post.query.order_by(
        Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template(template_name_or_list="home.html", posts=posts)


@main.route("/about")
def about():
    return render_template(template_name_or_list="about.html", title='About')
