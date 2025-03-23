from flask import Blueprint, request, jsonify
from ..services.chat_service import obter_resposta

chat_bp = Blueprint('chat', __name__)

@chat_bp.route("/chat", methods=["POST"])
def chat():
    """
    Endpoint para processar mensagens do chat.
    
    Returns:
        JSON: Resposta contendo a mensagem do chatbot
    """
    dados = request.get_json()
    pergunta = dados.get("pergunta", "")

    if not pergunta:
        return jsonify({"resposta": "Erro: Nenhuma pergunta fornecida"}), 400

    resposta = obter_resposta(pergunta)
    return jsonify({"resposta": resposta})

@chat_bp.route("/send_message", methods=["POST"])
def send_message():
    """
    Endpoint alternativo para enviar mensagens.
    
    Returns:
        JSON: Resposta contendo a mensagem do chatbot
    """
    data = request.get_json()
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({"response": "Erro: Nenhuma mensagem fornecida"}), 400

    resposta = obter_resposta(user_message)
    return jsonify({"response": resposta}) 