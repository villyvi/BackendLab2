from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_smorest import Api
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("../config.py", silent=True)

    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)

    from .models import User, Category, Record  
    from .routes import bp
    app.register_blueprint(bp)

    api = Api(app) 
    return app
