# config.py

import os
from dotenv import load_dotenv

# Tentukan path absolut ke direktori tempat file config.py ini berada
basedir = os.path.abspath(os.path.dirname(__file__))

# Secara eksplisit muat file .env dari path tersebut
# Ini adalah metode yang paling tahan banting
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    # Sekarang, os.environ.get() PASTI akan menemukan variabelnya
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False