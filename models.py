from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
DEFAULT_IMAGE_URL = "https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png"
def connect_db(app):
    db.app = app
    db.init_app(app)

"""Models for Blogly."""
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,
    primary_key=True,
    autoincrement=True)

    first_name = db.Column(db.String(20),
    nullable=False,
    )

    last_name = db.Column(db.String(20),
    nullable=False,
    )

    image_url = db.Column(db.String, nullable=False, default=DEFAULT_IMAGE_URL)
    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")


    @property
    def full_name(self):
        """Return full name of user."""


        return f"{self.first_name} {self.last_name}"
    
class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key =True, autoincrement= True)
    title = db.Column(db.Text, nullable=False,)
    content = db.Column(db.Text, nullable =False,)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user_id =db.Column(db.Integer, db.ForeignKey('users.id'))
    posted_tags= db.relationship('PostTag', backref="post")
   

class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key =True, autoincrement= True)
    name = db.Column(db.Text, nullable=False, unique=True)
    posted_tags= db.relationship('PostTag', backref="tags")
    posts = db.relationship('Post', secondary ="post_tags", backref='tags')

class PostTag(db.Model):
    __tablename__ = 'post_tags'
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)