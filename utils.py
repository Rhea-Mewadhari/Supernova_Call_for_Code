import json
from gradio_client import Client
import os

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

gradio_client = Client(os.getenv('MODAL_API'))

def predict_image(image_url):
    try:
        # Use Gradio client to predict
        result = gradio_client.predict(image_url, api_name="/predict")
        
        return result
    except Exception as e:
        return {"error": str(e)}

def predict_image(image_url):
    # Assuming you have a Gradio client that makes a prediction
    result_file_path = gradio_client.predict(image_url)
    
    # Read the result from the file path
    with open(result_file_path, 'r') as file:
        result = json.load(file)
    
    # Return the result as a dictionary
    return result