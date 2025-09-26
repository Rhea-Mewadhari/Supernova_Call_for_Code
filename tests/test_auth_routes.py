import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
import itsdangerous
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Supernova_Call_for_Code.routes.auth_routes import auth_bp

@pytest.fixture
def client(monkeypatch):
    app = Flask(__name__)
    app.secret_key = "testkey"
    app.register_blueprint(auth_bp)

    fake_users = MagicMock()
    fake_db = {"users": fake_users}
    monkeypatch.setattr("Supernova_Call_for_Code.routes.auth_routes.get_db", lambda: fake_db)

    app.extensions = {"mail": MagicMock()}

    return app.test_client(), fake_users, app

@patch("Supernova_Call_for_Code.routes.auth_routes.create_user_document", return_value={"doc": 1})
@patch("Supernova_Call_for_Code.routes.auth_routes.generate_token", return_value="tok")
@patch("Supernova_Call_for_Code.routes.auth_routes.send_confirmation_email")
def test_register_success(mock_send, mock_token, mock_doc, client):
    c, users, app = client
    users.find_one.return_value = None
    resp = c.post(
        "/register",
        data={"email": "a@b.com", "password": "x", "confirm": "x", "username": "alice"},
    )
    assert resp.status_code == 302
    users.insert_one.assert_called_once()
    mock_send.assert_called_once()

def test_register_passwords_dont_match(client):
    c, users, app = client
    resp = c.post(
        "/register",
        data={"email": "a@b.com", "password": "x", "confirm": "y"},
    )
    assert resp.status_code == 302
    users.insert_one.assert_not_called()

def test_register_email_already_exists(client):
    c, users, app = client
    users.find_one.return_value = {"email": "a@b.com"}
    resp = c.post(
        "/register",
        data={"email": "a@b.com", "password": "x", "confirm": "x"},
    )
    assert resp.status_code == 302
    users.insert_one.assert_not_called()

def test_confirm_email_success(client):
    c, users, app = client
    s = itsdangerous.URLSafeTimedSerializer(app.secret_key)
    token = s.dumps("a@b.com", salt="email-confirmation")
    resp = c.get(f"/confirm_email/{token}")
    assert resp.status_code == 302
    users.update_one.assert_called_once()

def test_confirm_email_expired(client, monkeypatch):
    c, users, app = client
    monkeypatch.setattr(
        "itsdangerous.URLSafeTimedSerializer.loads",
        lambda *a, **k: (_ for _ in ()).throw(itsdangerous.SignatureExpired("boom")),
    )
    resp = c.get("/confirm_email/badtoken")
    assert resp.status_code == 302

def test_confirm_email_invalid(client, monkeypatch):
    c, users, app = client
    monkeypatch.setattr(
        "itsdangerous.URLSafeTimedSerializer.loads",
        lambda *a, **k: (_ for _ in ()).throw(itsdangerous.BadTimeSignature("bad")),
    )
    resp = c.get("/confirm_email/badtoken")
    assert resp.status_code == 302

@patch("Supernova_Call_for_Code.routes.auth_routes.url_for", return_value="/home")
@patch("Supernova_Call_for_Code.routes.auth_routes.check_password_hash", return_value=True)
def test_login_success(mock_check, mock_url_for, client):
    c, users, app = client
    users.find_one.return_value = {
        "email": "a@b.com",
        "username": "alice",
        "password": "hashed",
        "active": True,
    }
    resp = c.post("/login", data={"email": "a@b.com", "password": "pw"})
    assert resp.status_code == 302
    assert resp.headers["Location"].endswith("/home")

def test_login_inactive_account(client):
    c, users, app = client
    users.find_one.return_value = {"email": "a@b.com", "active": False}
    resp = c.post("/login", data={"email": "a@b.com", "password": "pw"})
    assert resp.status_code == 302

@patch("Supernova_Call_for_Code.routes.auth_routes.render_template", return_value="login page")
@patch("Supernova_Call_for_Code.routes.auth_routes.check_password_hash", return_value=False)
def test_login_bad_password(mock_check, mock_render, client):
    c, users, app = client
    users.find_one.return_value = {
        "email": "a@b.com",
        "username": "alice",
        "password": "hashed",
        "active": True,
    }
    resp = c.post("/login", data={"email": "a@b.com", "password": "pw"})
    assert resp.status_code == 200
    assert b"login page" in resp.data
    mock_render.assert_called_once_with("login.html")

@patch("Supernova_Call_for_Code.routes.auth_routes.generate_token", return_value="tok")
@patch("Supernova_Call_for_Code.routes.auth_routes.send_password_reset_email")
def test_reset_request_user_found(mock_send, mock_token, client):
    c, users, app = client
    users.find_one.return_value = {"email": "a@b.com"}
    resp = c.post("/reset_password_request", data={"email": "a@b.com"})
    assert resp.status_code == 302
    mock_send.assert_called_once()

def test_reset_request_user_not_found(client):
    c, users, app = client
    users.find_one.return_value = None
    resp = c.post("/reset_password_request", data={"email": "a@b.com"})
    assert resp.status_code == 302

@patch("Supernova_Call_for_Code.routes.auth_routes.url_for", return_value="/login")
@patch("Supernova_Call_for_Code.routes.auth_routes.hash_password", return_value="hashedpw")
def test_reset_password_success(mock_hash, mock_url_for, client):
    c, users, app = client
    s = itsdangerous.URLSafeTimedSerializer(app.secret_key)
    token = s.dumps("a@b.com", salt="password-reset")
    resp = c.post(f"/reset_password/{token}", data={"password": "newpw"})
    assert resp.status_code == 302
    users.update_one.assert_called_once()

def test_reset_password_invalid_token(client, monkeypatch):
    c, users, app = client
    monkeypatch.setattr(
        "itsdangerous.URLSafeTimedSerializer.loads",
        lambda *a, **k: (_ for _ in ()).throw(itsdangerous.BadTimeSignature("bad")),
    )
    resp = c.post("/reset_password/badtoken", data={"password": "pw"})
    assert resp.status_code == 302