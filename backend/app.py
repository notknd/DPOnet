import subprocess
import sys
import os

def instalar_dependencias():
    caminho = os.path.join(os.path.dirname(__file__), "requirements.txt")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", caminho])
        print("Dependências instaladas com sucesso.")
    except subprocess.CalledProcessError as e:
        print("Erro ao instalar dependências:", e)
        sys.exit(1)

instalar_dependencias()

import os
from dotenv import load_dotenv
import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS

# Carregar variáveis de ambiente
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
print(f"API Key carregada: {api_key[:2]}...{api_key[-2:] if api_key else 'None'}")

if not api_key:
    print("ERRO: API Key não encontrada no arquivo .env")
else:
    try:
        genai.configure(api_key=api_key)
        print("Configuração do Gemini realizada com sucesso")
    except Exception as e:
        print(f"ERRO ao configurar Gemini: {str(e)}")

# Configuração do Flask
app = Flask(__name__)
CORS(app)

# Modelo Gemini Pro
try:
    modelo = genai.GenerativeModel("gemini-1.5-flash")
    print("Modelo Gemini carregado com sucesso")
except Exception as e:
    print(f"ERRO ao carregar modelo: {str(e)}")
    modelo = None

# Contexto inicial
contexto = """
Você é um assistente virtual especializado na empresa DPO.net.
Seu objetivo é fornecer informações claras e resumidas sobre os serviços da DPO.net,
focando em temas como LGPD, proteção de dados, consultoria e assessoria jurídica.

Sempre fale em português brasileiro
Se não souber a resposta, diga que só pode responder sobre a DPO.net.
Se a pergunta for ofensiva ou inadequada, peça que o usuário mantenha o respeito.
"""

# Função para obter resposta do modelo Gemini
def obter_resposta_como_gemini(pergunta):
    # Construção do contexto completo com a pergunta
    contexto_completo = contexto + "\nUsuário: " + pergunta + "\nChatbot:"

    try:
        # Gerar resposta usando o modelo Gemini
        resposta = modelo.generate_content(contexto_completo)
        return resposta.text
    except Exception as e:
        return f"Erro ao comunicar com a API: {str(e)}"

# Função para verificar macros
def verificar_macros(pergunta):
    # Dicionário de macros
    macros = {
        "contato": "Para entrar em contato conosco, envie um e-mail para contato@dpnet.com.br.",
        "comunicar": "Para entrar em contato conosco, envie um e-mail para contato@dpnet.com.br.",
        "comunicação": "Para entrar em contato conosco, envie um e-mail para contato@dpnet.com.br.",
        "suporte": "Nosso suporte pode ser acessado pelo e-mail suporte@dpnet.com.br.",
        "horário": "Nosso horário de atendimento é de segunda a sexta-feira, das 9h às 18h.",
        "site": "Você pode acessar nosso site em www.dpnet.com.br para mais informações.",
        "agendar": "Para agendar uma conversa e obter mais informações sobre nossos serviços, por favor, visite nosso site em www.dponet.com.br e preencha o formulário de contato. Você também pode entrar em contato conosco pelo telefone +55 (11) 5199-3959 ou pelo e-mail dpo@netbr.com.br. Nossa equipe entrará em contato o mais breve possível para agendar uma reunião.",
        "agendamento": "Para agendar uma conversa e obter mais informações sobre nossos serviços, por favor, visite nosso site em www.dponet.com.br e preencha o formulário de contato. Você também pode entrar em contato conosco pelo telefone +55 (11) 5199-3959 ou pelo e-mail dpo@netbr.com.br. Nossa equipe entrará em contato o mais breve possível para agendar uma reunião.",
        "cnpj": "O CNPJ da DPO.net é 36.487.128/0001-79.",
        "sede": "A DPOnet tem uma sede em Marília, São Paulo, localizada na Avenida das Esmeraldas 3865, Torre Tókyo, salas 103 e 104",
        "local": "A DPOnet tem uma sede em Marília, São Paulo, localizada na Avenida das Esmeraldas 3865, Torre Tókyo, salas 103 e 104",
        "localização": "A DPOnet tem uma sede em Marília, São Paulo, localizada na Avenida das Esmeraldas 3865, Torre Tókyo, salas 103 e 104",
        "endereço": "A DPOnet tem uma sede em Marília, São Paulo, localizada na Avenida das Esmeraldas 3865, Torre Tókyo, salas 103 e 104"
    }

    # Verificar se a pergunta contém alguma palavra-chave para macro
    pergunta = pergunta.lower()
    for chave, resposta in macros.items():
        if chave in pergunta:
            return resposta

    # Caso não tenha encontrado, retornar None
    return None

# Função para obter resposta, considerando macros primeiro, depois o modelo Gemini
def obter_resposta(pergunta):
    # Verificar se a pergunta se encaixa em alguma macro
    resposta_macro = verificar_macros(pergunta)
    if resposta_macro:
        return resposta_macro

    # Se não for uma macro, utilizar o modelo Gemini
    return obter_resposta_como_gemini(pergunta)

# Rota para obter a chave da API
@app.route("/api/config")
def get_config():
    if not api_key:
        print("ERRO: API Key não encontrada ao tentar retornar configuração")
        return jsonify({
            'status': 'error',
            'message': 'API key não configurada no servidor'
        }), 500
    
    print("Retornando configuração com sucesso")
    return jsonify({
        'status': 'success',
        'apiKey': api_key,
        'message': 'Configuração carregada com sucesso'
    })

# Rota para comunicação com o frontend
@app.route("/chat", methods=["POST"])
def chat():
    dados = request.get_json()
    pergunta = dados.get("pergunta", "")

    if not pergunta:
        return jsonify({"resposta": "Erro: Nenhuma pergunta fornecida"}), 400

    # Obter resposta baseada na pergunta
    resposta = obter_resposta(pergunta)
    return jsonify({"resposta": resposta})

# Rota para enviar mensagens
@app.route("/send_message", methods=["POST"])
def send_message():
    if not modelo:
        return jsonify({
            'status': 'error',
            'response': 'Modelo não está inicializado corretamente'
        }), 500

    try:
        data = request.get_json()
        user_message = data.get("message", "")

        if not user_message:
            return jsonify({
                'status': 'error',
                'response': 'Mensagem vazia'
            }), 400

        print(f"Mensagem recebida: {user_message}")
        
        # Construção do contexto completo com a pergunta
        contexto_completo = f"{contexto}\nUsuário: {user_message}\nChatbot:"
        
        # Gerar resposta usando o modelo Gemini
        resposta = modelo.generate_content(contexto_completo)
        print(f"Resposta gerada com sucesso: {resposta.text[:100]}...")
        
        return jsonify({
            'status': 'success',
            'response': resposta.text
        })
    except Exception as e:
        print(f"ERRO ao processar mensagem: {str(e)}")
        return jsonify({
            'status': 'error',
            'response': f'Erro ao processar mensagem: {str(e)}'
        }), 500

if __name__ == "__main__":
    app.run(debug=True)