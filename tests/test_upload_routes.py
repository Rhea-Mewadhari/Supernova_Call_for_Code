import io
import pytest
from unittest.mock import patch, MagicMock
from flask import Flask, session
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Supernova_Call_for_Code.routes.upload_routes import upload_bp

@pytest.fixture
def client(monkeypatch):
    app = Flask(__name__)
    app.secret_key = "testkey"
    app.register_blueprint(upload_bp)

    app.config["CLOUDINARY"] = {
        "cloud_name": "demo",
        "api_key": "fake",
        "api_secret": "fake"
    }

    fake_db = {"chat_images": MagicMock()}
    monkeypatch.setattr("Supernova_Call_for_Code.routes.upload_routes.get_db", lambda: fake_db)

    return app.test_client(), fake_db, app

def test_upload_no_file(client):
    c, db, app = client
    resp = c.post("/upload_image", data={})
    assert resp.status_code == 400
    assert "No file" in resp.get_json()["error"]

@patch("Supernova_Call_for_Code.routes.upload_routes.cloudinary.uploader.upload")
@patch("Supernova_Call_for_Code.routes.upload_routes.predict_image", return_value={"pred": 1})
def test_upload_success(mock_predict, mock_upload, client):
    c, db, app = client
    mock_upload.return_value = {"url": "http://img"}

    with c.session_transaction() as sess:
        sess["email"] = "a@b.com"

    fake_file = (io.BytesIO(b"data"), "test.jpg")
    resp = c.post(
        "/upload_image",
        data={"file": fake_file, "sessionId": "s1"},
        content_type="multipart/form-data"
    )

    assert resp.status_code == 200
    data = resp.get_json()
    assert data["image_url"] == "http://img"
    assert data["predictions"] == {"pred": 1}
    db["chat_images"].insert_one.assert_called_once()
    mock_predict.assert_called_once_with("http://img")

@patch("Supernova_Call_for_Code.routes.upload_routes.cloudinary.uploader.upload")
@patch("Supernova_Call_for_Code.routes.upload_routes.predict_image", return_value={"pred": 1})
def test_upload_no_session_email(mock_predict, mock_upload, client):
    c, db, app = client
    mock_upload.return_value = {"url": "http://img"}

    fake_file = (io.BytesIO(b"data"), "test.jpg")
    resp = c.post(
        "/upload_image",
        data={"file": fake_file, "sessionId": "s1"},
        content_type="multipart/form-data"
    )

    assert resp.status_code == 403
    assert "Login required" in resp.get_json()["error"]
    db["chat_images"].insert_one.assert_not_called()

@patch("Supernova_Call_for_Code.routes.upload_routes.cloudinary.uploader.upload", side_effect=Exception("upload fail"))
def test_upload_cloudinary_failure(mock_upload, client):
    c, db, app = client

    with c.session_transaction() as sess:
        sess["email"] = "a@b.com"

    fake_file = (io.BytesIO(b"data"), "test.jpg")
    resp = c.post(
        "/upload_image",
        data={"file": fake_file, "sessionId": "s1"},
        content_type="multipart/form-data"
    )

    assert resp.status_code == 500 or "error" in resp.get_json()