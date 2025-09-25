import json
import pytest
from unittest.mock import patch, MagicMock, mock_open

from Supernova_Call_for_Code.services import prediction_service

@pytest.fixture(autouse=True)
def clear_cache():
    """Ensure the cache is clean before every test."""
    prediction_service._gradio_client_cache.clear()
    yield
    prediction_service._gradio_client_cache.clear()

@pytest.fixture
def dummy_app(monkeypatch):
    """Fake current_app with config for MODAL_API."""
    class DummyApp:
        config = {"MODAL_API": "http://fake.api"}
    monkeypatch.setattr(prediction_service, "current_app", DummyApp)

@patch.object(prediction_service, "Client")
def test_get_gradio_client_creates_and_caches(mock_client, dummy_app):
    fake_client = MagicMock()
    mock_client.return_value = fake_client

    client1 = prediction_service.get_gradio_client()
    assert client1 is fake_client
    mock_client.assert_called_once_with("http://fake.api")

    client2 = prediction_service.get_gradio_client()
    assert client2 is fake_client
    mock_client.assert_called_once() 

@patch.object(prediction_service, "Client")
def test_get_gradio_client_different_url_creates_new_client(mock_client, dummy_app, monkeypatch):
    fake_client1 = MagicMock()
    fake_client2 = MagicMock()
    mock_client.side_effect = [fake_client1, fake_client2]

    client1 = prediction_service.get_gradio_client()
    assert client1 is fake_client1

    class OtherApp:
        config = {"MODAL_API": "http://other.api"}
    monkeypatch.setattr(prediction_service, "current_app", OtherApp)

    client2 = prediction_service.get_gradio_client()
    assert client2 is fake_client2
    assert "http://fake.api" in prediction_service._gradio_client_cache
    assert "http://other.api" in prediction_service._gradio_client_cache

@patch.object(prediction_service, "get_gradio_client")
def test_predict_image_success(mock_get_client, dummy_app, tmp_path):
    fake_client = MagicMock()
    result_file = tmp_path / "result.json"
    result_data = {"label": "cat"}
    result_file.write_text(json.dumps(result_data))

    fake_client.predict.return_value = str(result_file)
    mock_get_client.return_value = fake_client

    result = prediction_service.predict_image("http://image.jpg")

    fake_client.predict.assert_called_once_with("http://image.jpg")
    assert result == {"label": "cat"}

@patch.object(prediction_service, "get_gradio_client")
def test_predict_image_file_missing(mock_get_client, dummy_app):
    fake_client = MagicMock()
    fake_client.predict.return_value = "non_existent.json"
    mock_get_client.return_value = fake_client

    result = prediction_service.predict_image("http://image.jpg")
    assert "error" in result
    assert "No such file" in result["error"] or "non_existent.json" in result["error"]

@patch.object(prediction_service, "get_gradio_client")
def test_predict_image_client_error(mock_get_client, dummy_app):
    fake_client = MagicMock()
    fake_client.predict.side_effect = Exception("predict fail")
    mock_get_client.return_value = fake_client

    result = prediction_service.predict_image("http://bad.jpg")
    assert result == {"error": "predict fail"}