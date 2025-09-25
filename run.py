# run.py

from flask import Flask
from flask_mail import Mail
from config import Config
from routes import register_routes
import cloudinary
#from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(Config)

#CORS(app)

# Init Flask-Mail
mail = Mail(app)

# Configure Cloudinary
cloudinary.config(**Config.CLOUDINARY)

# Register routes
register_routes(app)

if __name__ == '__main__':
    app.run(debug=True)