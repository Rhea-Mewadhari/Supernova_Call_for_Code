# app/routes/page_routes.py

from flask import Blueprint, render_template, redirect, url_for, session
from services.db_service import get_db 
import json

page_bp = Blueprint('page', __name__)

@page_bp.route('/')
def index():
    return render_template('index.html')

@page_bp.route('/home')
def home():
    if 'email' in session:
        db = get_db()  #  Access within app context
        user = db['users'].find_one({'email': session['email']})
        return render_template('home.html', user=user)
    return redirect(url_for('auth.login'))

@page_bp.route('/about')
def about():
    if 'email' in session:
        db = get_db()  #  Access within app context
        user = db['users'].find_one({'email': session['email']})

        with open('static/disease_data.json') as f:
            disease_data = json.load(f)

        return render_template('about.html', user=user, disease_data=disease_data)
    return redirect(url_for('auth.login'))

@page_bp.route('/history')
def history():
    if 'email' in session:
        db = get_db()
        email = session['email']
        user = db['users'].find_one({'email': email})

        # Fetch disease data from the chat_images collection
        disease_data = list(db['chat_images'].find({'email': email})) if email else []

        return render_template('history.html', user=user, disease_data=disease_data)
    
    return redirect(url_for('auth.login'))

@page_bp.route('/newchat', methods=['GET', 'POST'])
def newchat():
    if 'username' in session:
        db = get_db()
        email = session['email']
        user = db['users'].find_one({'email': email})
        return render_template('newchat.html', user=user)
    else:
        return redirect(url_for('auth.login'))

@page_bp.route('/logout')
def logout():
    session.clear()
    return render_template('logout.html')