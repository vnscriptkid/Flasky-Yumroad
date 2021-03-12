from flask import Blueprint, render_template
from werkzeug.exceptions import abort

from app.models import Product

products = Blueprint('products', __name__)


@products.route('/')
def index():
    all_products = Product.query.all()
    return render_template('products/index.html', products=all_products)


@products.route('/<int:product_id>')
def details(product_id):
    product = Product.query.get(product_id)
    if not product:
        abort(404)
    return render_template('products/details.html', product=product)


@products.errorhandler(404)
def not_found(exception):
    return render_template('products/404.html'), 404

