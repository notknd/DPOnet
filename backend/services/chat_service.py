import google.generativeai as genai
from ..config.config import API_KEY, CHATBOT_CONTEXT, MACROS
from ..config.knowledge_base import KNOWLEDGE_BASE

# Configurar o modelo Gemini
genai.configure(api_key=API_KEY)
modelo = genai.GenerativeModel("gemini-1.5-pro")

def formatar_contexto_completo(pergunta):
    """
    Formata o contexto completo incluindo a base de conhecimento.
    
    Args:
        pergunta (str): A pergunta do usuário
        
    Returns:
        str: Contexto completo formatado
    """
    # Formatar informações da base de conhecimento
    conhecimento = f"""
    Informações sobre a DPO.net: 
    {KNOWLEDGE_BASE['sobre_dpo']['descricao']}
    
    Serviços oferecidos:
    {', '.join(KNOWLEDGE_BASE['sobre_dpo']['servicos'])}
    
    Informações sobre LGPD:
    {KNOWLEDGE_BASE['lgpd']['descricao']}
    
    Pontos importantes sobre LGPD:
    {', '.join(KNOWLEDGE_BASE['lgpd']['pontos_importantes'])}
    
    Informações de contato:
    Email: {KNOWLEDGE_BASE['contato']['email']}
    Telefone: {KNOWLEDGE_BASE['contato']['telefone']}
    Endereço: {KNOWLEDGE_BASE['contato']['endereco']}
    Horário: {KNOWLEDGE_BASE['contato']['horario']}
    
    Perguntas frequentes:
    """
    
    # Adicionar FAQs
    for faq in KNOWLEDGE_BASE['faq']['perguntas_comuns']:
        conhecimento.upper() += f"\nP: {faq['pergunta']}\nR: {faq['resposta']}\n"
    
    return f"{CHATBOT_CONTEXT}\n\n{conhecimento.upper()}\n\nUsuário: {pergunta}\nChatbot:"

def obter_resposta_como_gemini(pergunta):
    """
    Obtém uma resposta do modelo Gemini para a pergunta fornecida.
    
    Args:
        pergunta (str): A pergunta do usuário
        
    Returns:
        str: A resposta gerada pelo modelo
    """
    try:
        contexto_completo = formatar_contexto_completo(pergunta)
        resposta = modelo.generate_content(contexto_completo)
        return resposta.text
    except Exception as e:
        return f"Erro ao comunicar com a API: {str(e)}"

def verificar_macros(pergunta):
    """
    Verifica se a pergunta corresponde a alguma macro predefinida.
    
    Args:
        pergunta (str): A pergunta do usuário
        
    Returns:
        str or None: A resposta da macro se encontrada, None caso contrário
    """
    pergunta = pergunta.lower()
    
    # Verificar macros do dicionário
    for chave, resposta in MACROS.items():
        if chave in pergunta:
            return resposta
            
    # Verificar na base de conhecimento
    if "sobre" in pergunta or "quem é" in pergunta:
        return KNOWLEDGE_BASE['sobre_dpo']['descricao']
    elif "lgpd" in pergunta:
        return KNOWLEDGE_BASE['lgpd']['descricao']
    elif "serviços" in pergunta or "servicos" in pergunta:
        return f"A DPO.net oferece os seguintes serviços: {', '.join(KNOWLEDGE_BASE['sobre_dpo']['servicos'])}"
    elif "contato" in pergunta or "falar" in pergunta:
        return f"Para entrar em contato conosco:\nEmail: {KNOWLEDGE_BASE['contato']['email']}\nTelefone: {KNOWLEDGE_BASE['contato']['telefone']}\nEndereço: {KNOWLEDGE_BASE['contato']['endereco']}\nHorário: {KNOWLEDGE_BASE['contato']['horario']}"
    
    return None

def obter_resposta(pergunta):
    """
    Obtém uma resposta para a pergunta do usuário, verificando primeiro macros
    e depois usando o modelo Gemini.
    
    Args:
        pergunta (str): A pergunta do usuário
        
    Returns:
        str: A resposta gerada
    """
    resposta_macro = verificar_macros(pergunta)
    if resposta_macro:
        return resposta_macro

    return obter_resposta_como_gemini(pergunta) 