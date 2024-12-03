from .db import db


class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fullname = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    avatar = db.Column(db.String(255), default=None)
    role = db.Column(db.Enum('user', 'admin'), nullable=False, default='user')
    created_at = db.Column(db.TIMESTAMP, nullable=False,
                           server_default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP, nullable=False, server_default=db.func.current_timestamp(),
                           onupdate=db.func.current_timestamp())

    is_active = db.Column(db.Boolean, default=False)

    def __init__(self, fullname, username, password, email, avatar=None, role='user', is_active=False):
        self.fullname = fullname
        self.username = username
        self.email = email
        self.password = password
        self.avatar = avatar
        self.role = role
        self.is_active = is_active

    def get_id(self):
        return self.id


class Books(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey(
        'category.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    publish_year = db.Column(db.Integer, nullable=False)
    author = db.Column(db.String(100), nullable=False)
    publisher = db.Column(db.String(100), nullable=False)
    summary = db.Column(db.Text)
    cover = db.Column(db.String(255), default=None)
    view_count = db.Column(db.Integer, default=0)
    download_count = db.Column(db.Integer, default=0)
    file_path = db.Column(db.String(255), default=None)
    average_rating = db.Column(db.Float, default=0)

    def __init__(self, category_id, title, publish_year, author, publisher, summary=None, cover=None, view_count=0, download_count=0, file_path=None, average_rating=0):
        self.category_id = category_id
        self.title = title
        self.publish_year = publish_year
        self.author = author
        self.publisher = publisher
        self.summary = summary
        self.cover = cover
        self.view_count = view_count
        self.download_count = download_count
        self.file_path = file_path
        self.average_rating = average_rating


class Category(db.Model):
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)
    image = db.Column(db.String(255))

    def __init__(self, category, image=None):
        self.category = category
        self.image = image


class Comments(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_on = db.Column(db.TIMESTAMP, nullable=True,
                           server_default=db.func.current_timestamp())
    updated_on = db.Column(db.TIMESTAMP, nullable=True, server_default=db.func.current_timestamp(
    ), onupdate=db.func.current_timestamp())

    def __init__(self, book_id, user_id, content):
        self.book_id = book_id
        self.user_id = user_id
        self.content = content


class Favorites(db.Model):
    __tablename__ = 'favorites'

    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    added_on = db.Column(db.TIMESTAMP, nullable=True,
                         server_default=db.func.current_timestamp())

    def __init__(self, book_id, user_id):
        self.book_id = book_id
        self.user_id = user_id


class Request(db.Model):
    __tablename__ = 'request'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    book_title = db.Column(db.String(255), nullable=False)
    book_description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.TIMESTAMP, nullable=True,
                           server_default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP, nullable=True, server_default=db.func.current_timestamp(
    ), onupdate=db.func.current_timestamp())
    is_approved = db.Column(db.Boolean, nullable=True)

    def __init__(self, user_id, book_title, book_description, is_approved=None):
        self.user_id = user_id
        self.book_title = book_title
        self.book_description = book_description
        self.is_approved = is_approved
