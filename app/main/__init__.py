from flask import Flask
from flask_mongoengine import MongoEngine
from flask_bcrypt import Bcrypt
from .config import config_by_name

mdb = MongoEngine()
app = Flask(__name__)
bcrypt = Bcrypt()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    db = MongoEngine()

    with app.app_context():
        db.init_app(app)
        bcrypt.init_app(app)

    return app

