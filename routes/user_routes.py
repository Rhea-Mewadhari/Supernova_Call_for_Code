# app/routes/user_routes.py

from flask import Blueprint, session, request, jsonify, render_template, flash, redirect, url_for, current_app
from services.user_service import update_user_profile, upload_profile_picture, store_feedback
from services.email_service import send_recommendation_email
from services.db_service import get_db  
import cloudinary.uploader

user_bp = Blueprint('user', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@user_bp.route('/profile', methods=['GET', 'POST'])
def profile():
    db = get_db()
    users = db['users']
    email = session.get('email')
    user = users.find_one({'email': email})
    max_size = current_app.config.get('MAX_CONTENT_LENGTH')

    if request.method == 'POST':
        updates = {}
        if 'profile_picture' in request.files:
            file = request.files['profile_picture']
            new_url, error = upload_profile_picture(file, max_size, user.get('profile_picture'))
            if error:
                flash(error, 'danger')
            else:
                updates['profile_picture'] = new_url

        for field in ['illness', 'allergies', 'medication']:
            value = request.form.get(field)
            if value:
                updates[field] = value

        update_user_profile(db, email, updates)
        flash("Profile updated!", 'success')

    return render_template("profile.html", user=user)

@user_bp.route('/submit-feedback', methods=['POST'])
def submit_feedback():
    if 'email' not in session:
        return jsonify({"message": "Unauthorized"}), 403

    db = get_db()
    csat = request.form.get('csat')
    feedback_text = request.form.get('feedbackText')
    store_feedback(db, session['email'], csat, feedback_text)

    return jsonify({"message": "Feedback submitted", "category": "success"}), 200

@user_bp.route('/recommend', methods=['POST'])
def recommend():
    if 'email' not in session:
        return jsonify({"message": "Login required", "category": "danger"}), 403

    name = request.form['recommendName']
    recipient = request.form['recommendEmail']
    
    mail = current_app.extensions['mail']
    send_recommendation_email(mail, recipient, name, session['username'])

    return jsonify({"message": "Email sent!", "category": "success"})

@user_bp.route('/update_profile', methods=['POST'])
def update_profile():
    if 'email' not in session:
        return jsonify({'status': 'error', 'message': 'User not logged in'}), 401

    db = get_db()
    email = session['email']
    user = db['users'].find_one({"email": email})

    update_fields = {}

    # Get MAX_CONTENT_LENGTH from config
    max_content_length = current_app.config.get('MAX_CONTENT_LENGTH')
    if max_content_length is None:
        return jsonify({'status': 'error', 'message': 'MAX_CONTENT_LENGTH not set in config'}), 500

    # Handle profile picture upload
    if 'profile_picture' in request.files:
        file = request.files['profile_picture']
        if file and allowed_file(file.filename):
            file_size = len(file.read())
            file.seek(0)
            if file_size > max_content_length:
                return jsonify({'status': 'error', 'message': 'File size exceeds 10 MB limit'}), 400
            try:
                upload_result = cloudinary.uploader.upload(file)
                image_url = upload_result['url']

                # Delete old profile picture
                old_picture = user.get('profile_picture', 'user.png')
                if old_picture and old_picture != "user.png":
                    public_id = old_picture.rsplit('/', 1)[-1].split('.')[0]
                    cloudinary.uploader.destroy(public_id)

                update_fields['profile_picture'] = image_url
            except Exception as e:
                return jsonify({'status': 'error', 'message': f'Error uploading file: {str(e)}'}), 500

    # Handle other fields
    for field in ['allergies', 'illness', 'medication']:
        value = request.form.get(field)
        if value:
            update_fields[field] = value

    # Update DB
    if update_fields:
        db['users'].update_one({"email": email}, {"$set": update_fields})

    return jsonify({
        'status': 'success',
        'message': 'Profile updated successfully!',
        'profile_picture': update_fields.get('profile_picture', user.get('profile_picture')),
        'allergies': update_fields.get('allergies', user.get('allergies')),
        'illness': update_fields.get('illness', user.get('illness')),
        'medication': update_fields.get('medication', user.get('medication')),
    })