import pytest
from unittest.mock import patch, MagicMock
from flask import Flask

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Supernova_Call_for_Code.routes.chat_routes import chat_bp

@pytest.fixture
def client(monkeypatch):
    app = Flask(__name__)
    app.register_blueprint(chat_bp)

    fake_db = {
        "chat_history": MagicMock(),
        "sessions": MagicMock(),
    }
    monkeypatch.setattr("Supernova_Call_for_Code.routes.chat_routes.get_db", lambda: fake_db)

    return app.test_client(), fake_db

def test_send_custom_chatbot_success(client):
    c, db = client
    resp = c.post("/custom-chatbot/send", json={"label": "foo"})
    assert resp.status_code == 200
    assert "Received label: foo" in resp.get_json()["response"]

def test_send_custom_chatbot_missing_label(client):
    c, db = client
    resp = c.post("/custom-chatbot/send", json={})
    assert resp.status_code == 200
    assert "Received label: None" in resp.get_json()["response"]

def test_save_chat_history_success(client):
    c, db = client
    resp = c.post("/save-chat-history", json={"session": "123", "msg": "hi"})
    assert resp.status_code == 200
    db["chat_history"].insert_one.assert_called_once()

def test_get_session_found(client):
    c, db = client
    db["sessions"].find_one.return_value = {"sessionId": "abc", "data": 1}
    resp = c.get("/get-session/abc")
    assert resp.status_code == 200
    assert resp.get_json()["data"] == 1

def test_get_session_not_found(client):
    c, db = client
    db["sessions"].find_one.return_value = None
    resp = c.get("/get-session/missing")
    assert resp.status_code == 404
    assert "Not found" in resp.get_json()["error"]

def test_get_chat_history_found(client):
    c, db = client
    fake_result = {"_id": 123, "email": "a@b.com", "session_id": "s1"}
    db["chat_history"].find_one.return_value = fake_result
    resp = c.post("/get-chat-history", json={"email": "a@b.com", "session_id": "s1"})
    assert resp.status_code == 200
    result = resp.get_json()
    assert result["_id"] == "123"  

def test_get_chat_history_not_found(client):
    c, db = client
    db["chat_history"].find_one.return_value = None
    resp = c.post("/get-chat-history", json={"email": "a@b.com", "session_id": "s1"})
    assert resp.status_code == 404

@patch("Supernova_Call_for_Code.routes.chat_routes.VectorDBService")
def test_ask_success(mock_vdb, client):
    c, db = client
    mock_service = MagicMock()
    mock_service.ask.return_value = {"answer": "42", "sources": [{"content": "x"}]}
    mock_vdb.from_config.return_value = mock_service

    resp = c.post("/ask", json={"question": "life?", "session_id": "s1"})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["answer"] == "42"
    assert data["session_id"] == "s1"

def test_ask_no_question(client):
    c, db = client
    resp = c.post("/ask", json={"session_id": "s1"})
    assert resp.status_code == 400
    assert "No question" in resp.get_json()["error"]

@patch("Supernova_Call_for_Code.routes.chat_routes.VectorDBService")
def test_ask_vectordb_failure(mock_vdb, client):
    c, db = client
    mock_vdb.from_config.side_effect = Exception("boom")

    resp = c.post("/ask", json={"question": "hi", "session_id": "s1"})
    assert resp.status_code == 500
    assert "boom" in resp.get_json()["error"]