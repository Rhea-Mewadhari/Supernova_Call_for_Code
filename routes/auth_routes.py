# routes/auth_routes.py

from flask import Blueprint, request, render_template, session, redirect, url_for, flash, current_app
from services.user_service import create_user_document, hash_password
from services.email_service import send_confirmation_email, send_password_reset_email, generate_token
from services.db_service import get_db  
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadTimeSignature
from werkzeug.security import check_password_hash

auth_bp = Blueprint('auth', __name__)

def get_users_collection():
    return get_db()['users']

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    users = get_users_collection()

    if request.method == 'POST':
        data = request.form.to_dict()

        if data['password'] != data['confirm']:
            flash("Passwords don't match", 'danger')
            return redirect(url_for('auth.register'))

        if users.find_one({"email": data['email']}):
            flash("Email already registered", 'danger')
            return redirect(url_for('auth.register'))

        user_doc = create_user_document(data)
        users.insert_one(user_doc)

        token = generate_token(current_app.config['SECRET_KEY'], data['email'], 'email-confirmation')

        mail = current_app.extensions['mail']
        send_confirmation_email(mail, data['email'], data['username'], token)

        flash("Confirmation email sent", 'info')
        return redirect(url_for('auth.check_email'))

    return render_template("register.html")

@auth_bp.route('/check_your_email')
def check_email():
    return render_template("check_your_email.html")

@auth_bp.route('/confirm_email/<token>')
def confirm_email(token):
    users = get_users_collection()

    try:
        s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        email = s.loads(token, salt='email-confirmation', max_age=3600)
        users.update_one({"email": email}, {"$set": {"active": True}})
        flash("Account activated", 'success')
    except SignatureExpired:
        flash("Token expired", 'danger')
    except BadTimeSignature:
        flash("Invalid token", 'danger')

    return redirect(url_for('auth.login'))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    users = get_users_collection()

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = users.find_one({'email': email})

        if not user or not user.get("active"):
            flash("Invalid or inactive account", 'danger')
            return redirect(url_for('auth.login'))

        if check_password_hash(user['password'], password):
            session['email'] = user['email']
            session['username'] = user['username']
            return redirect(url_for('page.home'))
        else:
            flash("Invalid credentials", 'danger')

    return render_template("login.html")

@auth_bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_request():
    users = get_users_collection()

    if request.method == 'POST':
        email = request.form['email']
        user = users.find_one({"email": email})

        if user:
            token = generate_token(current_app.config['SECRET_KEY'], email, 'password-reset')
            mail = current_app.extensions['mail']
            send_password_reset_email(mail, email, token)

        return redirect(url_for('auth.check_email'))

    return render_template("reset_password_request.html")

@auth_bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    users = get_users_collection()
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])

    try:
        email = s.loads(token, salt='password-reset', max_age=3600)
    except (SignatureExpired, BadTimeSignature):
        flash("Invalid or expired link", 'danger')
        return redirect(url_for('auth.reset_request'))

    if request.method == 'POST':
        new_password = request.form['password']
        users.update_one({"email": email}, {"$set": {"password": hash_password(new_password)}})
        flash("Password reset successfully", 'success')
        return redirect(url_for('auth.login'))

    return render_template("reset_password.html")