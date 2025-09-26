import io
import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Supernova_Call_for_Code.services import user_service

@pytest.fixture
def dummy_app(monkeypatch):
    class DummyApp:
        config = {
            "MAX_CONTENT_LENGTH": 5, 
            "CLOUDINARY": {"cloud_name": "demo", "api_key": "123", "api_secret": "abc"}
        }
    monkeypatch.setattr(user_service, "current_app", DummyApp)

@pytest.fixture
def fake_file():
    """Return a file-like object for upload tests."""
    return io.BytesIO(b"abc")  # 3 bytes

@patch.object(user_service, "get_db")
def test_update_user_profile_calls_update_one(mock_get_db):
    fake_users = MagicMock()
    mock_get_db.return_value = {"users": fake_users}

    user_service.update_user_profile("user@example.com", {"name": "Alice"})

    fake_users.update_one.assert_called_once_with(
        {"email": "user@example.com"}, {"$set": {"name": "Alice"}}
    )

@patch.object(user_service.cloudinary, "uploader")
def test_upload_profile_picture_success(mock_uploader, dummy_app, fake_file):
    mock_uploader.upload.return_value = {"url": "http://new.pic"}
    new_url, err = user_service.upload_profile_picture(fake_file)
    assert new_url == "http://new.pic"
    assert err is None
    mock_uploader.upload.assert_called_once()

@patch.object(user_service.cloudinary, "uploader")
def test_upload_profile_picture_too_large(mock_uploader, dummy_app):
    big_file = io.BytesIO(b"abcdef")  # 6 bytes > MAX_CONTENT_LENGTH
    new_url, err = user_service.upload_profile_picture(big_file)
    assert new_url is None
    assert "exceeds limit" in err
    mock_uploader.upload.assert_not_called()

@patch.object(user_service.cloudinary, "uploader")
def test_upload_profile_picture_existing_non_user_triggers_destroy(mock_uploader, dummy_app, fake_file):
    mock_uploader.upload.return_value = {"url": "http://new.pic"}
    current_url = "http://cloudinary.com/otherpic.png"
    new_url, err = user_service.upload_profile_picture(fake_file, current_picture_url=current_url)
    assert new_url == "http://new.pic"
    mock_uploader.destroy.assert_called_once()

@patch.object(user_service.cloudinary, "uploader")
def test_upload_profile_picture_upload_failure(mock_uploader, dummy_app, fake_file):
    mock_uploader.upload.side_effect = Exception("upload fail")
    new_url, err = user_service.upload_profile_picture(fake_file)
    assert new_url is None
    assert "upload fail" in err

def test_hash_password_creates_hash():
    hashed = user_service.hash_password("mypassword")
    assert hashed != "mypassword"
    assert hashed.startswith("pbkdf2:sha256")

def test_create_user_document_contains_expected_fields():
    data = {
        "first_name": "Alice",
        "last_name": "Smith",
        "username": "alice",
        "email": "alice@example.com",
        "gender": "F",
        "password": "secret"
    }
    doc = user_service.create_user_document(data)
    assert doc["first_name"] == "Alice"
    assert doc["email"] == "alice@example.com"
    assert "pbkdf2:sha256" in doc["password"]
    assert doc["active"] is False
    assert doc["illness"] == "NA"
    assert "profile_picture" in doc

def test_store_feedback_inserts_with_timestamp():
    fake_db = {"feedback": MagicMock()}
    user_service.store_feedback(fake_db, "bob@example.com", 5, "Great app!")
    args, kwargs = fake_db["feedback"].insert_one.call_args
    inserted_doc = args[0]
    assert inserted_doc["email"] == "bob@example.com"
    assert inserted_doc["csat"] == 5
    assert inserted_doc["feedback_text"] == "Great app!"
    assert isinstance(inserted_doc["timestamp"], datetime)