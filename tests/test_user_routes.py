import io
import pytest
from unittest.mock import patch, MagicMock
from flask import Flask, session
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Supernova_Call_for_Code.routes.user_routes import user_bp, allowed_file

@pytest.fixture
def client(monkeypatch):
    app = Flask(__name__)
    app.secret_key = "testkey"
    app.register_blueprint(user_bp)

    monkeypatch.setattr(
        "Supernova_Call_for_Code.routes.user_routes.render_template",
        lambda t, **k: f"rendered {t} {k}"
    )

    fake_users = MagicMock()
    fake_users.find_one.return_value = {"email": "test@example.com", "profile_picture": "user.png"}
    fake_users.update_one.return_value = None

    fake_db = {"users": fake_users, "feedback": MagicMock()}

    monkeypatch.setattr("Supernova_Call_for_Code.services.db_service.get_db", lambda: fake_db)
    monkeypatch.setattr("services.db_service.get_db", lambda: fake_db)

    app.config["MAX_CONTENT_LENGTH"] = 1024 * 1024
    return app.test_client(), fake_db, app

def test_allowed_file_true_and_false():
    assert allowed_file("pic.jpg")
    assert allowed_file("pic.PNG")
    assert not allowed_file("pic.txt")
    assert not allowed_file("noext")

@patch("Supernova_Call_for_Code.routes.user_routes.upload_profile_picture", return_value=("newurl", None))
@patch("Supernova_Call_for_Code.routes.user_routes.update_user_profile")
def test_profile_post_success(mock_update, mock_upload, client):
    c, db, app = client
    with c.session_transaction() as sess:
        sess["email"] = "test@example.com"

    fake_file = (io.BytesIO(b"abc"), "pic.jpg")
    resp = c.post(
        "/profile",
        data={"profile_picture": fake_file, "illness": "flu"},
        content_type="multipart/form-data",
    )
    assert resp.status_code == 200
    mock_upload.assert_called_once()
    mock_update.assert_called_once()

@patch("Supernova_Call_for_Code.routes.user_routes.upload_profile_picture", return_value=(None, "fail"))
@patch("Supernova_Call_for_Code.routes.user_routes.update_user_profile")
def test_profile_post_upload_error(mock_update, mock_upload, client):
    c, db, app = client
    with c.session_transaction() as sess:
        sess["email"] = "test@example.com"

    fake_file = (io.BytesIO(b"abc"), "pic.jpg")
    resp = c.post(
        "/profile",
        data={"profile_picture": fake_file},
        content_type="multipart/form-data",
    )
    assert resp.status_code == 200
    mock_update.assert_not_called()  

def test_profile_get(client):
    c, db, app = client
    with c.session_transaction() as sess:
        sess["email"] = "test@example.com"
    resp = c.get("/profile")
    assert resp.status_code == 200
    assert "profile.html" in resp.get_data(as_text=True)

@patch("Supernova_Call_for_Code.routes.user_routes.store_feedback")
def test_submit_feedback_success(mock_store, client):
    c, db, app = client
    with c.session_transaction() as sess:
        sess["email"] = "test@example.com"
    resp = c.post("/submit-feedback", data={"csat": "5", "feedbackText": "good"})
    assert resp.status_code == 200
    mock_store.assert_called_once_with("test@example.com", "5", "good")

def test_submit_feedback_unauthorized(client):
    c, db, app = client
    resp = c.post("/submit-feedback", data={"csat": "5"})
    assert resp.status_code == 403

@patch("Supernova_Call_for_Code.routes.user_routes.send_recommendation_email")
def test_recommend_success(mock_send, client):
    c, db, app = client
    with c.session_transaction() as sess:
        sess["email"] = "test@example.com"
        sess["username"] = "alice"
    app.extensions = {"mail": MagicMock()}
    resp = c.post("/recommend", data={"recommendName": "Bob", "recommendEmail": "bob@example.com"})
    assert resp.status_code == 200
    mock_send.assert_called_once()

def test_recommend_not_logged_in(client):
    c, db, app = client
    resp = c.post("/recommend", data={"recommendName": "Bob", "recommendEmail": "bob@example.com"})
    assert resp.status_code == 403

@patch("Supernova_Call_for_Code.routes.user_routes.update_user_profile")
@patch("Supernova_Call_for_Code.routes.user_routes.cloudinary.uploader.upload", return_value={"url": "http://img"})
@patch("Supernova_Call_for_Code.routes.user_routes.cloudinary.uploader.destroy")
def test_update_profile_success(mock_destroy, mock_upload, mock_update, client):
    c, db, app = client
    with c.session_transaction() as sess:
        sess["email"] = "test@example.com"

    fake_file = (io.BytesIO(b"abc"), "pic.jpg")
    resp = c.post(
        "/update_profile",
        data={"profile_picture": fake_file, "illness": "flu"},
        content_type="multipart/form-data",
    )
    assert resp.status_code == 200
    mock_update.assert_called_once()

def test_update_profile_not_logged_in(client):
    c, db, app = client
    resp = c.post("/update_profile")
    assert resp.status_code == 401

def test_update_profile_missing_config(client):
    c, db, app = client
    app.config.pop("MAX_CONTENT_LENGTH")
    with c.session_transaction() as sess:
        sess["email"] = "test@example.com"
    resp = c.post("/update_profile")
    assert resp.status_code == 500

@patch("Supernova_Call_for_Code.routes.user_routes.cloudinary.uploader.upload", side_effect=Exception("fail"))
def test_update_profile_upload_error(mock_upload, client):
    c, db, app = client
    with c.session_transaction() as sess:
        sess["email"] = "test@example.com"
    fake_file = (io.BytesIO(b"abc"), "pic.jpg")
    resp = c.post(
        "/update_profile",
        data={"profile_picture": fake_file},
        content_type="multipart/form-data",
    )
    assert resp.status_code == 500
    assert "Error uploading file" in resp.get_json()["message"]