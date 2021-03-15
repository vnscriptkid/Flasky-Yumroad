import sentry_sdk
from flask import Flask, render_template
from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
from webassets.loaders import PythonLoader as PythonAssetsLoader

from app import assets
from app.blueprints.checkout import checkout_bp
from app.blueprints.landing import landing_bp
from app.blueprints.products import products
from app.blueprints.rq_dashboard import rq_blueprint
from app.blueprints.stores import store_bp
from app.blueprints.users import user_bp
from app.config import configurations
from app.extensions import db, csrf, login_manager, migrate, mail, checkout, assets_env, rq2, debug_toolbar, cache


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
    rq2.init_app(app)
    debug_toolbar.init_app(app)
    cache.init_app(app)

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
    app.register_blueprint(landing_bp)
    app.register_blueprint(rq_blueprint, url_prefix="/rq")

    # errors monitoring
    if app.config.get("SENTRY_DSN"):
        sentry_sdk.init(
            dsn=app.config["SENTRY_DSN"],
            integrations=[FlaskIntegration(), SqlalchemyIntegration()]
        )

    # errors handling
    @app.errorhandler(401)
    def unauthorized_error(error):
        return render_template('errors/401.html'), 401

    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        return render_template('errors/500.html'), 500

    return app

# FLASK_APP=app:create_app('dev') flask run

