from app.extensions import mail, rq2
from flask_mail import Message


@rq2.job
def send_email(subject, sender, to_emails, html_body, text_body=None, **kwargs):
    message = Message(subject, sender=sender, recipients=to_emails, **kwargs)

    message.body = text_body or html_body
    message.html = html_body

    return mail.send(message)