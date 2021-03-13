from flask import render_template
from flask_mail import Message
from app.extensions import mail

DEFAULT_FROM = ('Yumroad', 'yumroad@example.com')


def send_basic_welcome_message(recipient_email):
    message = Message('Welcome to YumYum',
                      sender=DEFAULT_FROM,
                      recipients=[recipient_email],
                      body="Thanks for joining. Let us know if you have any questions!")
    mail.send(message)


def send_welcome_message(user):
    message = Message('Welcome to YumYum {}'.format(user.store.name),
                      sender=DEFAULT_FROM,
                      recipients=[user.email])

    message.html = render_template('emails/welcome_basic.html', store=user.store)
    mail.send(message)


def send_pretty_welcome_message(user):
    message = Message('Welcome to YumYum {}'.format(user.store.name),
                      sender=DEFAULT_FROM,
                      recipients=[user.email])

    message.html = render_template('emails/welcome_pretty.html', store=user.store)
    mail.send(message)
