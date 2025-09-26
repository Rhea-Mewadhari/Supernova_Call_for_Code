import json
import pytest
from unittest.mock import MagicMock, mock_open, patch
from flask import Flask, Blueprint
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Supernova_Call_for_Code.routes.page_routes import page_bp

@pytest.fixture
def client(monkeypatch):
    app = Flask(__name__)
    app.secret_key = "testkey"
    app.register_blueprint(page_bp)

    auth_bp = Blueprint("auth", __name__)
    @auth_bp.route("/login")
    def login():
        return "login"
    app.register_blueprint(auth_bp, url_prefix="/auth")

    monkeypatch.setattr(
        "Supernova_Call_for_Code.routes.page_routes.render_template",
        lambda template, **kwargs: f"rendered {template} with {kwargs}"
    )

    fake_db = {"users": MagicMock(), "chat_images": MagicMock()}
    monkeypatch.setattr("Supernova_Call_for_Code.routes.page_routes.get_db", lambda: fake_db)

    return app.test_client(), fake_db, app

def test_index_route(client):
    c, db, app = client
    resp = c.get("/")
    assert resp.status_code == 200
    assert "index.html" in resp.get_data(as_text=True)

def test_home_with_session(client):
    c, db, app = client
    with c.session_transaction() as sess:
        sess["email"] = "a@b.com"
    db["users"].find_one.return_value = {"email": "a@b.com"}
    resp = c.get("/home")
    assert resp.status_code == 200
    assert "home.html" in resp.get_data(as_text=True)

def test_home_without_session(client):
    c, db, app = client
    resp = c.get("/home")
    assert resp.status_code == 302

@patch("builtins.open", new_callable=mock_open, read_data=json.dumps({"disease": "flu"}))
def test_about_with_session(mock_file, client):
    c, db, app = client
    with c.session_transaction() as sess:
        sess["email"] = "a@b.com"
    db["users"].find_one.return_value = {"email": "a@b.com"}
    resp = c.get("/about")
    assert resp.status_code == 200
    assert "about.html" in resp.get_data(as_text=True)

def test_about_without_session(client):
    c, db, app = client
    resp = c.get("/about")
    assert resp.status_code == 302

def test_history_with_session(client):
    c, db, app = client
    with c.session_transaction() as sess:
        sess["email"] = "a@b.com"
    db["users"].find_one.return_value = {"email": "a@b.com"}
    db["chat_images"].find.return_value = [{"id": 1}]
    resp = c.get("/history")
    assert resp.status_code == 200
    assert "history.html" in resp.get_data(as_text=True)

def test_history_without_session(client):
    c, db, app = client
    resp = c.get("/history")
    assert resp.status_code == 302

def test_newchat_with_username_session(client):
    c, db, app = client
    with c.session_transaction() as sess:
        sess["username"] = "alice"
        sess["email"] = "a@b.com"
    db["users"].find_one.return_value = {"email": "a@b.com"}
    resp = c.get("/newchat")
    assert resp.status_code == 200
    assert "newchat.html" in resp.get_data(as_text=True)

def test_newchat_without_username(client):
    c, db, app = client
    resp = c.get("/newchat")
    assert resp.status_code == 302

def test_logout_clears_session(client):
    c, db, app = client
    with c.session_transaction() as sess:
        sess["email"] = "a@b.com"
    resp = c.get("/logout")
    assert resp.status_code == 200
    assert "logout.html" in resp.get_data(as_text=True)
    with c.session_transaction() as sess:
        assert "email" not in sess