# routes/upload_routes.py

from flask import Blueprint, request, session, jsonify, current_app
from services.prediction_service import predict_image
from services.db_service import get_db
from datetime import datetime
import cloudinary
import cloudinary.uploader

upload_bp = Blueprint('upload', __name__)

@upload_bp.route('/upload_image', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({"error": "No file"}), 400

    file = request.files['file']

    # Configure Cloudinary from config
    cloudinary.config(**current_app.config['CLOUDINARY'])

    # Upload to Cloudinary
    upload_result = cloudinary.uploader.upload(file)
    image_url = upload_result['url']

    # Predict from image
    predictions = predict_image(image_url)

    # Get session/email
    email = session.get('email')
    session_id = request.form.get('sessionId')

    if not email:
        return jsonify({"error": "Login required"}), 403

    # Insert into MongoDB
    db = get_db()
    chat_images = db['chat_images']

    doc = {
        'email': email,
        'image_url': image_url,
        'timestamp': datetime.utcnow().isoformat(),
        'predictions': predictions,
        'session_id': session_id
    }

    result = chat_images.insert_one(doc)

    return jsonify({
        '_id': str(result.inserted_id),
        'image_url': image_url,
        'predictions': predictions
    })