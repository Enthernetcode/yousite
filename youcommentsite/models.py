from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    date_registered = db.Column(db.DateTime, default=db.func.current_timestamp())
    youtube_accounts = db.relationship('YouTubeAccount', backref='user', lazy=True)
    comments = db.relationship('Comment', backref='user', lazy=True)

class YouTubeAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    credentials_file_path = db.Column(db.String(255), nullable=False)
    token_file_path = db.Column(db.String(255), nullable=False)

class CommentFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    video_id = db.Column(db.String(255), nullable=False)
    comment_text = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=db.func.current_timestamp())
    