from urllib.parse import unquote

import stripe
from flask import url_for


class Checkout:
    def __init__(self, app=None):
        if app:
            self.init_app(app)

    def init_app(self, app):
        stripe.api_key = app.config.get('STRIPE_SECRET_KEY')
        self.publishable_key = app.config.get('STRIPE_PUBLISHABLE_KEY')
        self.webhook_key = app.config.get('STRIPE_WEBHOOK_KEY')

    def create_session(self, product):
        if not product.price_cents:
            return
        success_url = unquote(url_for('products.post_checkout', product_id=product.id,
                                      session_id='{CHECKOUT_SESSION_ID}',
                                      status='success',
                                      _external=True))
        failure_url = unquote(url_for('products.post_checkout', product_id=product.id,
                                      session_id='{CHECKOUT_SESSION_ID}',
                                      status='cancel',
                                      _external=True))
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            client_reference_id=product.id,
            line_items=[{
                'name': product.name,
                'description': product.description,
                'amount': product.price_cents,
                'currency': 'usd',
                'images': [product.primary_image_url],
                'quantity': 1,
            }],
            mode='payment',
            success_url=success_url,
            cancel_url=failure_url,
        )
        return session

    def parse_webhook(self, payload, headers):
        received_sig = headers.get("Stripe-Signature", None)

        return stripe.Webhook.construct_event(
            payload, received_sig, self.webhook_key
        )

    def get_customer(self, customer_id):
        return stripe.Customer.retrieve(customer_id)

