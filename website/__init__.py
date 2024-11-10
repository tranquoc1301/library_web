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

    app.config['JWT_SECRET_KEY'] = os.environ.get(
        'JWT_SECRET_KEY', 'mysecret')  # Set your secret key

    # Khởi tạo Mail với app
    mail.init_app(app)

    # Khởi tạo JWT
    jwt = JWTManager(app)
    # Khởi tạo database và schema
    db.init_app(app)
    jwt.init_app(app)
    ma.init_app(app)

    # Đăng ký blueprint
    app.register_blueprint(views)
    app.register_blueprint(auth)

    return app
