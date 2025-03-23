"""
Base de conhecimento para o chatbot da DPO.net
"""

KNOWLEDGE_BASE = {
    "sobre_dpo": {
        "descricao": """
        A DPO.net é uma empresa especializada em proteção de dados e conformidade com a LGPD.
        Oferecemos serviços de consultoria, assessoria jurídica e implementação de programas de privacidade.
        """,
        "servicos": [
            "Consultoria LGPD",
            "Assessoria Jurídica",
            "Implementação de Programas de Privacidade",
            "Treinamentos em Proteção de Dados",
            "Auditoria de Conformidade"
        ], 
        "detalhes": [
            "Consultoria LGPD: Análise de riscos, implementação de políticas e procedimentos, treinamento de equipes.",
            "Assessoria Jurídica: Representação em litígios, defesa de ações judiciais e orientação jurídica sobre a LGPD.",
            "Implementação de Programas de Privacidade: Desenvolvimento de documentos de privacidade, políticas e procedimentos.",
            "Treinamentos em Proteção de Dados: Capacitação para a LGPD, auditoria de dados e implementação de políticas de privacidade."
        ],
        
    },
    "lgpd": {
        "descricao": """
        A Lei Geral de Proteção de Dados (LGPD) é a legislação brasileira que regula o tratamento de dados pessoais.
        A DPO.net auxilia empresas a se adequarem a esta legislação.
        """,
        "pontos_importantes": [
            "Consentimento do titular",
            "Direitos dos titulares",
            "Obrigações das empresas",
            "Segurança dos dados",
            "Relatório de Impacto"
        ],
        
    },
    "contato": {
        "email": "contato@dpnet.com.br",
        "telefone": "+55 (11) 5199-3959",
        "endereco": "Avenida das Esmeraldas 3865, Torre Tókyo, salas 103 e 104, Marília - SP",
        "horario": "Segunda a sexta-feira, das 9h às 18h"
    },
    "faq": {
        "perguntas_comuns": [
            {
                "pergunta": "O que é LGPD?",
                "resposta": "A LGPD é a Lei Geral de Proteção de Dados, que regula o tratamento de dados pessoais no Brasil."
            },
            {
                "pergunta": "Quais são os direitos dos titulares de dados?",
                "resposta": "Os titulares têm direito a acessar, corrigir, excluir, portar, revogar consentimento e solicitar a anonimização de seus dados."
            },
            {
                "pergunta": "Como a DPO.net pode ajudar minha empresa?",
                "resposta": "Oferecemos consultoria completa para adequação à LGPD, desde a análise inicial até a implementação de programas de privacidade."
            }
        ]
    }
} 