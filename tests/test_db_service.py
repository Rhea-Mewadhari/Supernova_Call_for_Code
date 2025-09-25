import pytest
from unittest.mock import patch, MagicMock

from Supernova_Call_for_Code.services import db_service

@patch("Supernova_Call_for_Code.services.db_service.MongoClient")
def test_get_db_success(mock_mongo, monkeypatch):
    """Ensure get_db returns the 'user_database' DB object when URI is present."""
    fake_db = MagicMock()
    fake_client = {"user_database": fake_db}
    mock_mongo.return_value = fake_client

    class DummyApp:
        config = {"URI": "mongodb://localhost:27017"}

    monkeypatch.setattr(db_service, "current_app", DummyApp)

    db = db_service.get_db()

    mock_mongo.assert_called_once_with("mongodb://localhost:27017")
    assert db is fake_db

@patch("Supernova_Call_for_Code.services.db_service.MongoClient")
def test_get_db_missing_uri_config(mock_mongo, monkeypatch):
    """If URI is missing in config, KeyError should be raised."""
    class DummyApp:
        config = {}

    monkeypatch.setattr(db_service, "current_app", DummyApp)

    with pytest.raises(KeyError):
        db_service.get_db()

    mock_mongo.assert_not_called()

@patch("Supernova_Call_for_Code.services.db_service.MongoClient", side_effect=Exception("bad uri"))
def test_get_db_invalid_uri(mock_mongo, monkeypatch):
    """If MongoClient init fails, the error should propagate."""
    class DummyApp:
        config = {"URI": "invalid://uri"}

    monkeypatch.setattr(db_service, "current_app", DummyApp)

    with pytest.raises(Exception, match="bad uri"):
        db_service.get_db()