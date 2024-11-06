from flask import Flask
import os
from .db import db, ma
from .auth import auth
from flask_mail import Mail
from flask_jwt_extended import JWTManager
from .views import views

mail = Mail()


def create_app():
    app = Flask(__name__)
    app.config.from_object('website.config')  # Lấy cấu hình từ config.py

    # Khởi tạo Mail với app
    mail.init_app(app)

    # Khởi tạo JWT
    jwt = JWTManager(app)

    # Khởi tạo database và schema
    db.init_app(app)
    ma.init_app(app)

    # Đăng ký blueprint
    app.register_blueprint(views)
    app.register_blueprint(auth)
    # app.register_blueprint(books)
    # app.register_blueprint(category)
    # app.register_blueprint(comments)
    # app.register_blueprint(favorites)
    # app.register_blueprint(ratings)
    # app.register_blueprint(students)

    return app
