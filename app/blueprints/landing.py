from flask import Blueprint, render_template
import logging

from app.models import Store

logger = logging.getLogger(__name__)

landing_bp = Blueprint('landing', __name__)


@landing_bp.route('/')
def index():
    # This is a bad query, we'll optimize it later
    stores = Store.query.limit(3).all()
    return render_template('landing/index.html', stores=stores)


@landing_bp.route('/error')
def error():
    logger.warning("About to do a dangerous calculation", extra={'data': 1})
    1/0
