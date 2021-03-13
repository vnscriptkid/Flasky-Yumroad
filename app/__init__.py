from flask import Flask

from app.blueprints.products import products
from app.config import configurations
from app.extensions import db, csrf


def create_app(environment_name='dev'):
    app = Flask(__name__)
    app.config.from_object(configurations[environment_name])

    db.init_app(app)
    csrf.init_app(app)

    app.register_blueprint(products, url_prefix="/product")

    return app

# FLASK_ENV=development FLASK_APP=app:create_app('dev') flask run

