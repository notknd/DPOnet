from flask import Flask
from flask_cors import CORS
from routes.chat_routes import chat_bp
from config.config import API_KEY
import google.generativeai as genai

# Configurar o Gemini
genai.configure(api_key=API_KEY)

def create_app():
    """
    Cria e configura a aplicação Flask.
    
    Returns:
        Flask: Aplicação Flask configurada
    """
    app = Flask(__name__)
    CORS(app)
    
    # Registrar blueprints
    app.register_blueprint(chat_bp)
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)







