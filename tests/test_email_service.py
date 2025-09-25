import pytest
from unittest.mock import patch, MagicMock
from itsdangerous import URLSafeTimedSerializer

from Supernova_Call_for_Code.services import email_service

@pytest.fixture
def dummy_app(monkeypatch):
    """Fake Flask current_app with config values."""
    class DummyApp:
        config = {
            "APP_URL": "http://localhost:5000",
            "SECRET_KEY": "super-secret"
        }
    monkeypatch.setattr(email_service, "current_app", DummyApp)

@pytest.fixture
def fake_mail():
    """Fake Flask-Mail instance with a spy send method."""
    return MagicMock()

@patch.object(email_service, "render_template", return_value="<p>Confirm</p>")
@patch.object(email_service, "Message")
def test_send_confirmation_email_success(mock_msg, mock_render, dummy_app, fake_mail):
    msg_instance = MagicMock()
    mock_msg.return_value = msg_instance

    email_service.send_confirmation_email(fake_mail, "user@example.com", "alice", "abc123")

    mock_render.assert_called_once_with("activate.html", confirm_url="http://localhost:5000/confirm_email/abc123")
    mock_msg.assert_called_once_with("Please confirm your email address", recipients=["user@example.com"])
    assert msg_instance.html == "<p>Confirm</p>"
    fake_mail.send.assert_called_once_with(msg_instance)

@patch.object(email_service, "render_template", side_effect=Exception("template fail"))
def test_send_confirmation_email_template_fail(mock_render, dummy_app, fake_mail):
    with pytest.raises(Exception, match="template fail"):
        email_service.send_confirmation_email(fake_mail, "user@example.com", "alice", "abc123")

@patch.object(email_service, "render_template", return_value="<p>Recommendation</p>")
@patch.object(email_service, "Message")
def test_send_recommendation_email_success(mock_msg, mock_render, dummy_app, fake_mail):
    msg_instance = MagicMock()
    mock_msg.return_value = msg_instance

    email_service.send_recommendation_email(fake_mail, "friend@example.com", "Bob", "alice")

    mock_render.assert_called_once_with("recommend.html", name="Bob", username="alice", app_url="http://localhost:5000")
    mock_msg.assert_called_once()
    assert "Recommendation from alice" in mock_msg.call_args[1]["subject"]
    fake_mail.send.assert_called_once_with(msg_instance)

@patch.object(email_service, "render_template", return_value="<p>Reset</p>")
@patch.object(email_service, "Message")
def test_send_password_reset_email_success(mock_msg, mock_render, dummy_app, fake_mail):
    msg_instance = MagicMock()
    mock_msg.return_value = msg_instance

    email_service.send_password_reset_email(fake_mail, "user@example.com", "reset123")

    mock_render.assert_called_once_with("reset_password_email.html", reset_url="http://localhost:5000/reset_password/reset123")
    mock_msg.assert_called_once_with("Reset Your Password", recipients=["user@example.com"])
    assert msg_instance.html == "<p>Reset</p>"
    fake_mail.send.assert_called_once_with(msg_instance)

def test_generate_token_success(dummy_app):
    token = email_service.generate_token("user@example.com", "salt123")
    assert isinstance(token, str)
    assert "user@example.com" in URLSafeTimedSerializer("super-secret").loads(token, salt="salt123")


def test_generate_token_missing_secret(monkeypatch):
    class DummyApp:
        config = {"APP_URL": "http://localhost:5000"}
    monkeypatch.setattr(email_service, "current_app", DummyApp)

    with pytest.raises(KeyError):
        email_service.generate_token("user@example.com", "salt123")