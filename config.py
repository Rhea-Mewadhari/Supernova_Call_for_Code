# config.py

import os
from dotenv import load_dotenv

load_dotenv()  # Load from .env

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    URI = os.getenv('URI')

    # Mail
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True') == 'True'
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')

    # App Settings
    APP_URL = os.getenv('APP_URL')
    UPLOAD_FOLDER = os.path.join('static', 'uploads')
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024

    # Cloudinary
    CLOUDINARY = {
        'cloud_name': os.getenv('CLOUD_NAME'),
        'api_key': os.getenv('API_KEY'),
        'api_secret': os.getenv('API_SECRET'),
    }

    # Gradio / AI
    MODAL_API = os.getenv('MODAL_API')

    CHROMA_DB_DIR = os.getenv("CHROMA_DB_DIR", "chroma_db")
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
    LLM_MODEL = os.getenv("LLM_MODEL", "llama3")