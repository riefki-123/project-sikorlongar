# app/__init__.py

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config

# Inisialisasi ekstensi di luar factory
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'main.login'
login_manager.login_message = 'Silakan login untuk mengakses halaman ini.'
login_manager.login_message_category = 'info'

def create_app(config_class=Config):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)

    # Inisialisasi ekstensi dengan aplikasi
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # --- Bagian Penting ---
    # Import dan daftarkan blueprint DI DALAM factory
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    # Import models agar dikenali oleh user loader
    from . import models

    return app