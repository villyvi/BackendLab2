import os

DB_USER = os.environ.get("DB_USER", "villyvi")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "13333")
DB_NAME = os.environ.get("DB_NAME", "lab3_db")
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_PORT = os.environ.get("DB_PORT", 5432)

FLASK_DEBUG = True

SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
SQLALCHEMY_TRACK_MODIFICATIONS = False

API_TITLE = "Lab 3 API"
API_VERSION = "1.0"
OPENAPI_VERSION = "3.0.3" 