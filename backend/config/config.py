import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configurações da API
API_KEY = os.getenv("GOOGLE_API_KEY")

# Contexto do chatbot
CHATBOT_CONTEXT = """
Você é um assistente virtual especializado na empresa DPO.net.
Seu objetivo é fornecer informações claras e resumidas sobre os serviços da DPO.net,
focando em temas como LGPD, proteção de dados, consultoria e assessoria jurídica.

Se não souber a resposta, diga que só pode responder sobre a DPO.net.
Se a pergunta for ofensiva ou inadequada, peça que o usuário mantenha o respeito.
"""

# Macros de respostas
MACROS = {
    "contato": "Para entrar em contato conosco, envie um e-mail para contato@dpnet.com.br.",
    "comunicar": "Para entrar em contato conosco, envie um e-mail para contato@dpnet.com.br.",
    "comunicação": "Para entrar em contato conosco, envie um e-mail para contato@dpnet.com.br.",
    "suporte": "Nosso suporte pode ser acessado pelo e-mail suporte@dpnet.com.br.",
    "horário": "Nosso horário de atendimento é de segunda a sexta-feira, das 9h às 18h.",
    "site": "Você pode acessar nosso site em www.dpnet.com.br para mais informações.",
    "website": "Você pode acessar nosso site em www.dpnet.com.br para mais informações.",
    "agendar": "Para agendar uma conversa e obter mais informações sobre nossos serviços, por favor, visite nosso site em www.dponet.com.br e preencha o formulário de contato. Você também pode entrar em contato conosco pelo telefone +55 (11) 5199-3959 ou pelo e-mail dpo@netbr.com.br. Nossa equipe entrará em contato o mais breve possível para agendar uma reunião.",
    "agendamento": "Para agendar uma conversa e obter mais informações sobre nossos serviços, por favor, visite nosso site em www.dponet.com.br e preencha o formulário de contato. Você também pode entrar em contato conosco pelo telefone +55 (11) 5199-3959 ou pelo e-mail dpo@netbr.com.br. Nossa equipe entrará em contato o mais breve possível para agendar uma reunião.",
    "cnpj": "O CNPJ da DPO.net é 36.487.128/0001-79.",
    "sede": "A DPOnet tem uma sede em Marília, São Paulo, localizada na Avenida das Esmeraldas 3865, Torre Tókyo, salas 103 e 104",
    "local": "A DPOnet tem uma sede em Marília, São Paulo, localizada na Avenida das Esmeraldas 3865, Torre Tókyo, salas 103 e 104",
    "localização": "A DPOnet tem uma sede em Marília, São Paulo, localizada na Avenida das Esmeraldas 3865, Torre Tókyo, salas 103 e 104",
    "endereço": "A DPOnet tem uma sede em Marília, São Paulo, localizada na Avenida das Esmeraldas 3865, Torre Tókyo, salas 103 e 104"
} 