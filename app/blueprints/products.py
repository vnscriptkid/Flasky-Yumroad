from flask import Blueprint, render_template, request, url_for, flash
from flask_login import login_required, current_user
from werkzeug.exceptions import abort
from werkzeug.utils import redirect

from app.extensions import db, checkout
from app.forms import ProductForm
from app.models import Product

products = Blueprint('products', __name__)


@products.route('/')
def index():
    all_products = Product.query.all()
    return render_template('products/index.html', products=all_products)


@products.route('/<int:product_id>')
def details(product_id):
    product = Product.query.get_or_404(product_id)

    stripe_publishable_key = checkout.publishable_key
    stripe_session = checkout.create_session(product) or {}
    checkout_session_id = stripe_session.get('id')

    return render_template('products/details.html',
                           product=product,
                           stripe_publishable_key=stripe_publishable_key,
                           checkout_session_id=checkout_session_id)


@products.route('/<product_id>/post-checkout')
def post_checkout(product_id):
    product = Product.query.get_or_404(product_id)
    purchase_state = request.args.get('status')
    post_purchase_session_id = request.args.get('session_id')

    if purchase_state == 'success' and post_purchase_session_id:
        flash("Thanks for purchasing {}. You will receive an email shortly".format(product.name), 'success')
    elif purchase_state == 'cancel' and post_purchase_session_id:
        flash("There was an error while attempting to purchase this product. Try again", 'danger')

    return redirect(url_for('products.details', product_id=product_id))


@products.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = ProductForm()
    if form.validate_on_submit():
        price = form.price.data or 0
        product = Product(name=form.name.data,
                          description=form.description.data,
                          price_cents=int(price*100),
                          picture_url=form.picture_url.data,
                          creator=current_user,
                          store=current_user.store)
        db.session.add(product)
        db.session.commit()

        return redirect(url_for('products.details', product_id=product.id))
    return render_template('products/create.html', form=form)


@products.route('/<product_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(product_id):
    product = Product.query.get_or_404(product_id)
    form = ProductForm(obj=product)
    if form.validate_on_submit():
        product.name = form.name.data
        product.description = form.description.data
        db.session.add(product)
        db.session.commit()
        return redirect(url_for('.details', product_id=product.id))
    return render_template('products/edit.html', form=form, product=product)

