# services/user_service.py

import cloudinary.uploader
from werkzeug.security import generate_password_hash
from datetime import datetime
from flask import current_app
from services.db_service import get_db  

def update_user_profile(email, updates: dict):
    db = get_db()
    users = db['users']
    users.update_one({"email": email}, {"$set": updates})

def upload_profile_picture(file, current_picture_url=None):
    max_size = current_app.config.get('MAX_CONTENT_LENGTH')

    file_size = len(file.read())
    file.seek(0)

    if file_size > max_size:
        return None, "File size exceeds limit."

    try:
        cloudinary.config(**current_app.config['CLOUDINARY'])

        upload_result = cloudinary.uploader.upload(file)
        new_url = upload_result['url']

        if current_picture_url and "user" not in current_picture_url:
            public_id = current_picture_url.rsplit('/', 1)[-1].split('.')[0]
            cloudinary.uploader.destroy(public_id)

        return new_url, None
    except Exception as e:
        return None, str(e)

def hash_password(password: str):
    return generate_password_hash(password, method='pbkdf2:sha256')

def create_user_document(data):
    return {
        "first_name": data["first_name"],
        "last_name": data["last_name"],
        "username": data["username"],
        "email": data["email"],
        "gender": data["gender"],
        "password": hash_password(data["password"]),
        "active": False,
        "illness": "NA",
        "allergies": "NA",
        "medication": "NA",
        "profile_picture": ""
    }

def store_feedback(db, email, csat, feedback_text):
    db['feedback'].insert_one({
        'email': email,
        'csat': csat,
        'feedback_text': feedback_text,
        'timestamp': datetime.utcnow()
    })