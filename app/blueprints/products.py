from flask import Blueprint, render_template, request, url_for
from flask_wtf import form
from werkzeug.exceptions import abort
from werkzeug.utils import redirect

from app.extensions import db
from app.forms import ProductForm
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


@products.route('/create', methods=['GET', 'POST'])
def create():
    form = ProductForm()
    if form.validate_on_submit():
        product = Product(name=request.form['name'], description=request.form['description'])
        db.session.add(product)
        db.session.commit()
        return redirect(url_for('product.details', product_id=product.id))
    return render_template('products/create.html', form=form)


@products.errorhandler(404)
def not_found(exception):
    return render_template('products/404.html'), 404

