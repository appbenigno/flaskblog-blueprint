from datetime import datetime, timedelta
from flaskblog import db, login_manager
from flask import current_app
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import Integer, String, Text, DateTime, ForeignKey
from flask_login import UserMixin
import jwt
import pytz


# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(20), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     image_file = db.Column(db.String(20), nullable=False,
#                            default='default.jpg')
#     password = db.Column(db.String(60), nullable=False)
#     posts = db.relationship('Post', backref='author', lazy=True)

#     def __repr__(self) -> str:
#         return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class User(db.Model, UserMixin):
    id = mapped_column(Integer, primary_key=True)
    username = mapped_column(String(20), unique=True, nullable=False)
    email = mapped_column(String(120), unique=True, nullable=False)
    image_file = mapped_column(
        String(20), nullable=False, default='default.jpg')
    password = mapped_column(String(60), nullable=False)
    posts = relationship('Post', backref='author', lazy=True)

    def get_reset_token(self, expires_sec=180):
        # s = TimedSerializer(app.config['SECRET_KEY'], expires_sec)
        # return s.dumps({'user_id': id}).decode('utf-8')
        exp = datetime.now(tz=pytz.utc) + timedelta(seconds=expires_sec)
        reset_token = jwt.encode(payload={
                                 'user_id': self.id, 'exp': exp}, key=current_app.config['SECRET_KEY'], algorithm="HS256")
        return reset_token

    @staticmethod
    def verify_reset_token(token):
        # s = TimedSerializer(app.config['SECRET_KEY'])
        # try:
        #     user_id = s.loads(token)['user_id']
        # except:
        #     return None
        # return User.query.get(user_id)
        try:
            data = jwt.decode(
                jwt=token, key=current_app.config['SECRET_KEY'], algorithms=["HS256"])
            user_id = data.get('user_id')
        except:
            return None

        return User.query.get(user_id)

    def __repr__(self) -> str:
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


# class Post(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(100), nullable=False)
#     date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)
#     content = db.Column(db.Text, nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

#     def __repr__(self) -> str:
#         return f"Post('{self.title}', '{self.date_posted}')"

class Post(db.Model):
    id = mapped_column(Integer, primary_key=True)
    title = mapped_column(String(100), nullable=False)
    date_posted = mapped_column(DateTime, nullable=False, default=datetime.now)
    content = mapped_column(Text, nullable=False)
    user_id = mapped_column(Integer, ForeignKey('user.id'), nullable=False)

    def __repr__(self) -> str:
        return f"Post('{self.title}', '{self.date_posted}')"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
