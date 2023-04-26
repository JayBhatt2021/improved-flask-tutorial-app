"""Holds the database models."""
from flask_login import UserMixin

from . import db


class User(db.Model, UserMixin):
    """The User database model."""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    posts = db.relationship("Post", backref="user", passive_deletes=True)
    upvotes = db.relationship("Upvote", backref="user", passive_deletes=True)


class Post(db.Model):
    """The Post database model."""

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    title = db.Column(db.String(255), nullable=False)
    body = db.Column(db.String(255), nullable=False)
    author_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False
    )
    upvotes = db.relationship("Upvote", backref="post", passive_deletes=True)


class Upvote(db.Model):
    """The Upvote database model."""

    id = db.Column(db.Integer, primary_key=True)
    upvoter_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False
    )
    upvoted_post_id = db.Column(
        db.Integer,
        db.ForeignKey("post.id", ondelete="CASCADE"),
        nullable=False
    )
