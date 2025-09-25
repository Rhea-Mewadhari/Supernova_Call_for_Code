# services/prediction_service.py

import json
from gradio_client import Client
from flask import current_app

_gradio_client_cache = {}

def get_gradio_client():
    modal_api_url = current_app.config['MODAL_API']
    if modal_api_url not in _gradio_client_cache:
        _gradio_client_cache[modal_api_url] = Client(modal_api_url)
    return _gradio_client_cache[modal_api_url]

def predict_image(image_url: str):
    try:
        gradio_client = get_gradio_client()
        result_file_path = gradio_client.predict(image_url)
        with open(result_file_path, 'r') as file:
            result = json.load(file)
        return result
    except Exception as e:
        return {"error": str(e)}