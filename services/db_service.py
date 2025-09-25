# app/services/db_service.py

from flask import current_app
from pymongo import MongoClient

def get_db():
    """
    Returns the main user database from the configured Mongo URI.
    """
    uri = current_app.config['URI']
    client = MongoClient(uri)
    return client["user_database"]