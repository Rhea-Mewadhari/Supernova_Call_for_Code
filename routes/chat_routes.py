# app/routes/chat_routes.py

from flask import Blueprint, request, jsonify
from services.vectordb_service import VectorDBService
from services.db_service import get_db

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/custom-chatbot/send', methods=['POST'])
def send_custom_chatbot():
    data = request.get_json()
    label = data.get("label")
    return jsonify({"response": f"Received label: {label}. Starting flow..."})

@chat_bp.route('/save-chat-history', methods=['POST'])
def save_chat_history():
    data = request.json
    db = get_db()
    chat_history = db['chat_history']
    chat_history.insert_one(data)
    return jsonify({"message": "Saved"}), 200

@chat_bp.route('/get-session/<session_id>', methods=['GET'])
def get_session(session_id):
    db = get_db()
    sessions = db['sessions']
    session_data = sessions.find_one({"sessionId": session_id})
    if not session_data:
        return jsonify({"error": "Not found"}), 404
    return jsonify(session_data)

@chat_bp.route('/get-chat-history', methods=['POST'])
def get_chat_history():
    db = get_db()
    chat_history = db['chat_history']
    data = request.get_json()
    email = data.get("email")
    session_id = data.get("session_id")
    result = chat_history.find_one({'email': email, 'session_id': session_id})
    if result:
        result['_id'] = str(result['_id'])
        return jsonify(result)
    return jsonify({"error": "Not found"}), 404

@chat_bp.route('/ask', methods=['POST'])
def ask_llm():
    data = request.get_json()
    # Frontend still sends "question", we map it to "query"
    query = data.get('question', "")
    session_id = data.get('session_id')

    if not query:
        return jsonify({"error": "No question provided"}), 400

    try:
        vectordb = VectorDBService.from_config()
        result = vectordb.ask(query)

        return jsonify({
            "answer": result.get("answer"),
            "sources": result.get("sources", []),
            "session_id": session_id
        })

    except Exception as e:
        print(f"Error in /ask endpoint: {e}")
        return jsonify({"error": str(e)}), 500