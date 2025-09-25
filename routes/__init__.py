# app/routes/__init__.py

from flask import Blueprint

def register_routes(app):
    from .auth_routes import auth_bp
    from .user_routes import user_bp
    from .chat_routes import chat_bp
    from .upload_routes import upload_bp
    from .page_routes import page_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(upload_bp)
    app.register_blueprint(page_bp)