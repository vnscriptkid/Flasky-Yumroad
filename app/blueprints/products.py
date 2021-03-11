from flask import Blueprint, render_template

products = Blueprint('products', __name__)


@products.route('/')
def index():
    return "All Products: Coming soon"

