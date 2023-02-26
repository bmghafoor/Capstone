
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()


class Source(db.Model):
    __tablename__ = 'source'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.Text, nullable = False)


class News(db.Model):

    __tablename__ = 'news'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    title = db.Column(db.Text, nullable = False, unique = True)
    author = db.Column(db.Integer, db.ForeignKey('authors.id'), nullable = True)
    category = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable = True)
    source = db.Column(db.Integer, db.ForeignKey('source.id'), nullable = True)
    description = db.Column(db.Text, nullable = False)
    content = db.Column(db.Text, nullable = False)
    date = db.Column(db.DateTime, nullable = False)
    url = db.Column(db.Text, nullable = False)
    image = db.Column(db.Text)

    s = db.relationship('Source', foreign_keys='News.source', lazy = 'joined')
    a = db.relationship('Author', foreign_keys='News.author', lazy = 'joined')


class Likes(db.Model):
    """Mapping user likes to news."""

    __tablename__ = 'likes' 

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id', ondelete='cascade'))
    news_id = db.Column(db.Integer, db.ForeignKey('news.id', ondelete='cascade'),unique=True)


class User(db.Model):
    """User in the system."""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    email = db.Column(db.Text, nullable=False, unique=True)
    username = db.Column(db.Text,nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    likes = db.relationship('News', secondary = 'likes')


    def __repr__(self):
        return f"<User #{self.id}: {self.username}, {self.email}>"


    @classmethod
    def signup(cls, username, email, password):

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')
        user = User(username=username, email=email, password=hashed_pwd)

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False


class Author(db.Model):
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.Text, nullable = False)

class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.Text, nullable = False)


class User_Source(db.Model):
    __tablename__ = 'user_source'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id', ondelete='cascade'))
    source_id = db.Column(db.Integer,db.ForeignKey('source.id', ondelete='cascade'))

class User_Author(db.Model):
    __tablename__ = 'user_author'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id', ondelete='cascade'))
    author_id = db.Column(db.Integer,db.ForeignKey('authors.id', ondelete='cascade'))

class User_Category(db.Model):
    __tablename__ = 'user_category'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id', ondelete='cascade'))
    category_id = db.Column(db.Integer,db.ForeignKey('categories.id', ondelete='cascade'))



def connect_db(app):

    db.app = app
    db.init_app(app)
