from flask import Blueprint, render_template

from app.models import Store

store_bp = Blueprint('store', __name__)


@store_bp.route('/stores')
def index():
    stores = Store.query.all()
    return render_template('stores/index.html', stores=stores)


@store_bp.route('/store/<store_id>')
def show(store_id):
    store = Store.query.get_or_404(store_id)
    products = store.products
    return render_template('stores/show.html', store=store, products=products)

