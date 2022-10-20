"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_IMAGE_URL = "https://cdn.iconscout.com/icon/free/png-256/user-placeholder-866235.png"

def connect_db(app):
    """Connect to database."""

    app.app_context().push()
    db.app = app
    db.init_app(app)


class User(db.Model):
    """ User profile """

    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    first_name = db.Column(
        db.String(50),
        nullable=False,
    )
    last_name = db.Column(
        db.String(50),
        nullable=False,
    )
    image_url = db.Column(
        db.String(100),
        nullable=False,
        default=DEFAULT_IMAGE_URL
    )

# class Post(db.Model):
#     """Post to the blog"""

#     __tablename__ = "posts"

#     id = db.Column(
#         db.Integer,
#         primary_key=True,
#         autoincrement=True
#     )
#     title = db.Column(
#         db.String(50),
#         nullable=False
#     )
#     content = db.Column(
#         db.String(10000),
#         nullable=False
#     )
#     created_at = db.Column(
#         db.DateTime,
#         nullable=False,
#         default=db.func.now
#     )
#     user_id = db.Column(
#         db.ForeignKey('user.id'),
#         nullable=False
#     )
