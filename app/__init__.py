from flask import Flask
from app.config import configurations
from app.extensions import db


def create_app(environment_name='dev'):
    app = Flask(__name__)
    app.config.from_object(configurations[environment_name])
    db.init_app(app)
    return app

# FLASK_ENV=development FLASK_APP="app:create_app" flask run

