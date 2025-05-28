import { useState, useEffect } from 'react';

function MainLayout() {
  // Estados do chat
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [error, setError] = useState(null);
  const [apiKey, setApiKey] = useState(null);

  // Carrega a chave da API
  useEffect(() => {
    console.log('Iniciando carregamento da configuração...');
    fetch('http://localhost:5000/api/config')
      .then(response => {
        console.log('Resposta recebida:', response.status);
        if (!response.ok) {
          throw new Error(`Erro ao carregar configuração: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        if (data.apiKey) {
          setApiKey(data.apiKey);
          setError(null);
          console.log('Chave da API carregada com sucesso');
        } else {
          throw new Error('Chave da API não encontrada na resposta');
        }
      })
      .catch(err => {
        console.error('Erro ao carregar configuração:', err);
        setError('Erro ao carregar configuração do chatbot');
      });
  }, []);

  const toggleChat = () => {
    setIsOpen(!isOpen);
  };

  const sendMessage = async (e) => {
    e.preventDefault();
    if (!inputMessage.trim() || !apiKey) {
      if (!apiKey) {
        setError('Chave da API não disponível');
      }
      return;
    }

    const userMessage = inputMessage;
    setInputMessage('');
    setMessages(prev => [...prev, { text: userMessage, sender: 'user' }]);

    try {
      const response = await fetch('https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'x-goog-api-key': apiKey
        },
        body: JSON.stringify({
          contents: [{
            parts: [{
              text: userMessage
            }]
          }]
        })
      });

      if (!response.ok) {
        throw new Error(`Erro na API: ${response.status}`);
      }

      const data = await response.json();

      if (!data.candidates || !data.candidates[0] || !data.candidates[0].content || !data.candidates[0].content.parts || !data.candidates[0].content.parts[0]) {
        throw new Error('Resposta inválida da API');
      }

      const botResponse = data.candidates[0].content.parts[0].text;
      setMessages(prev => [...prev, { text: botResponse, sender: 'bot' }]);
    } catch (error) {
      console.error('Erro ao enviar mensagem:', error);
      setMessages(prev => [...prev, {
        text: 'Desculpe, ocorreu um erro ao processar sua mensagem. Por favor, tente novamente.',
        sender: 'bot'
      }]);
    }
  };

  return (
    <div className="container">
      <div className="sidebar">
        <ul>
          <li className="highlight"><i className="fi fi-rs-clipboard"></i>Relatórios</li>
          <li className="highlight"><i className="fi fi-rs-shield"></i>Canal de Comunicação</li>
          <li className="highlight"><i className="fi fi-rs-box-open"></i>Fornecedores</li>
          <li className="highlight"><i className="fi fi-rs-social-network"></i>Consentimentos</li>
          <li className="highlight"><i className="fi fi-rs-suitcase-alt"></i>Empresa</li>
          <li className="highlight"><i className="fi fi-rs-box"></i>Documentos</li>
          <li className="highlight"><i className="fi fi-rs-cookie-alt"></i>Cookies</li>
          <li className="highlight"><i className="fi fi-rs-user-lock"></i>Central da Privacidade</li>
        </ul>
        <button id="cda">Central De Acompanhamento</button>
      </div>

      <div className="main-content">
        <div className="header-main">
          <h1>Central de Acompanhamento</h1>
          <input type="text" placeholder="Buscar..." />
          <button><i className="fi fi-rs-interrogation"></i>Tutorial</button>
          <button className="filter"><i className="fi fi-rs-filter"></i>Filtros</button>
        </div>

        <section className="help-section">
          <div className="help-card">
            <span className="tag">Acompanhamento</span>
            <h3>Status do Processo</h3>
            <p>Veja o andamento do seu serviço.</p>
            <button>Visualizar Status</button>
          </div>
          <div className="help-card">
            <span className="tag">Acompanhamento</span>
            <h3>Downloads de Documentos</h3>
            <p>Acesse contratos e relatórios.</p>
            <button>Baixar Documentos</button>
          </div>
          <div className="help-card">
            <span className="tag">Acompanhamento</span>
            <h3>Histórico de Atendimento</h3>
            <p>Consulte interações anteriores.</p>
            <button>Ver Histórico</button>
          </div>
          <div className="help-card">
            <span className="tag">Acompanhamento</span>
            <h3>Checklist de Conformidade</h3>
            <p>Veja os próximos passos e obrigações.</p>
            <button>Acessar Checklist</button>
          </div>
          <div className="help-card">
            <span className="tag">Acompanhamento</span>
            <h3>Solicitação de Suporte</h3>
            <p>Abra um chamado rapidamente.</p>
            <button>Abrir Chamado</button>
          </div>
          <div className="help-card">
            <span className="tag">Acompanhamento</span>
            <h3>Gerenciamento de Incidentes</h3>
            <p>Gerencie incidentes de segurança relacionados a dados pessoais.</p>
            <button>Gerenciar</button>
          </div>
        </section>

        {/* Chatbot integrado */}
        <div className="chatbot-container">
          <button className="chatbot-toggle" onClick={toggleChat}>
            {isOpen ? '✕' : '💬'}
          </button>

          {isOpen && (
            <div className="chatbot-popup">
              <div className="chatbot-header">
                <h3>Assistente Virtual</h3>
                <button onClick={toggleChat} className="close-button">✕</button>
              </div>

              {error && (
                <div className="chatbot-error">
                  {error}
                </div>
              )}

              <div className="chatbot-messages">
                {messages.map((message, index) => (
                  <div
                    key={index}
                    className={`message ${message.sender === 'user' ? 'user-message' : 'bot-message'}`}
                  >
                    {message.text}
                  </div>
                ))}
              </div>

              <form onSubmit={sendMessage} className="chatbot-input">
                <input
                  type="text"
                  value={inputMessage}
                  onChange={(e) => setInputMessage(e.target.value)}
                  placeholder="Digite sua mensagem..."
                  disabled={!apiKey}
                />
                <button type="submit" disabled={!apiKey}>➤</button>
              </form>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default MainLayout; 