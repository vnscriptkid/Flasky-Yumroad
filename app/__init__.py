from flask import Flask
from webassets.loaders import PythonLoader as PythonAssetsLoader

from app import assets
from app.blueprints.checkout import checkout_bp
from app.blueprints.products import products
from app.blueprints.stores import store_bp
from app.blueprints.users import user_bp
from app.config import configurations
from app.extensions import db, csrf, login_manager, migrate, mail, checkout, assets_env


def create_app(environment_name='dev'):
    app = Flask(__name__)
    app.config.from_object(configurations[environment_name])

    # init extensions
    db.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    mail.init_app(app)
    checkout.init_app(app)
    # assets bundling
    assets_env.init_app(app)
    assets_loader = PythonAssetsLoader(assets)
    for name, bundle in assets_loader.load_bundles().items():
        assets_env.register(name, bundle)

    # register blueprints
    app.register_blueprint(products, url_prefix="/product")
    app.register_blueprint(user_bp)
    app.register_blueprint(store_bp)
    app.register_blueprint(checkout_bp)

    return app

# FLASK_ENV=development FLASK_APP=app:create_app('dev') flask run

