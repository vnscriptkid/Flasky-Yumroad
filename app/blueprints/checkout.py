from flask import Blueprint, request
from werkzeug.exceptions import abort

from app.email import send_purchase_email
from app.extensions import csrf, checkout
from app.models import Product

checkout_bp = Blueprint('checkout', __name__)


@checkout_bp.route('/webhooks/stripe', methods=['POST'])
@csrf.exempt # Because this request is coming over an external API
def stripe_webhook():
    event = checkout.parse_webhook(request.data.decode("utf-8"), request.headers)
    if event.type == 'checkout.session.completed':
        session = event['data']['object']
        customer = checkout.get_customer(session['customer'])
        if 'client_reference_id' not in session:
            abort(400, 'Unknown product for checkout')

        product_id = session['client_reference_id']
        product = Product.query.get(product_id)
        if not customer or not product:
            abort(400, 'Unknown product & customer')

        send_purchase_email(customer.email, product)
    return "OK", 200

