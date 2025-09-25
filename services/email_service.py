# services/email_service.py

from flask_mail import Message
from flask import render_template, current_app
from itsdangerous import URLSafeTimedSerializer

def send_confirmation_email(mail, email, username, token):
    confirm_url = current_app.config['APP_URL'] + f"/confirm_email/{token}"
    html = render_template('activate.html', confirm_url=confirm_url)
    msg = Message('Please confirm your email address', recipients=[email])
    msg.html = html
    mail.send(msg)

def send_recommendation_email(mail, recipient_email, name, username):
    app_url = current_app.config['APP_URL']
    email_body = render_template('recommend.html', name=name, username=username, app_url=app_url)
    msg = Message(
        subject=f"Recommendation from {username}",
        recipients=[recipient_email],
        html=email_body
    )
    mail.send(msg)

def send_password_reset_email(mail, email, token):
    reset_url = current_app.config['APP_URL'] + f"/reset_password/{token}"
    html = render_template('reset_password_email.html', reset_url=reset_url)
    msg = Message('Reset Your Password', recipients=[email])
    msg.html = html
    mail.send(msg)

def generate_token(email, salt):
    """
    Generates a time-sensitive token using the app's secret key.
    """
    secret_key = current_app.config['SECRET_KEY']
    serializer = URLSafeTimedSerializer(secret_key)
    return serializer.dumps(email, salt=salt)