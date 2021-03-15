from flask import Blueprint, render_template

from app.models import Store, Product

store_bp = Blueprint('store', __name__)


@store_bp.route('/stores')
def index():
    stores = Store.query.all()
    return render_template('stores/index.html', stores=stores)


@store_bp.route('/stores/<store_id>')
@store_bp.route('/stores/<store_id>/<int:page>')
def show(store_id, page=1):
    store = Store.query.get_or_404(store_id)
    per_page = 9
    products_pagination = Product.query.filter_by(store=store).paginate(page, per_page)
    return render_template('stores/show.html', store=store, products_pagination=products_pagination)

