const sendChatBtn = document.querySelector(".chat-input span");
//  class="show-chatbot"
const API_KEY = "AIzaSyCe7DIqiZ4e2AnH-jp0S3JYPxeP3eGyWzw";
let UserMessage;

// constantes e eventos necessários
const chatInput = document.querySelector(".chat-input textarea");
const chatbox = document.querySelector(".chatbox");

// contantes | eventos que abrem, fecham o chat e definem um limite para o text area
const chatBotToggler = document.querySelector(".chatbot-toggler");
const chatBotCloseBtn = document.querySelector(".close-btn");

chatBotToggler.addEventListener("click", () => document.body.classList.toggle("show-chatbot"))
chatBotCloseBtn.addEventListener("click", () => document.body.classList.remove("show-chatbot"))


// cria um elemento Li (listed order) que contem a mensagem digitada
const createChatLi = (message, className) =>{
    const chatLi = document.createElement("li");
    chatLi.classList.add("chat", className);
    let chatContent = className === "outgoing" ? `<p></p>` : `<span class="material-symbols-outlined">smart_toy</span><p></p>`;
    chatLi.innerHTML = chatContent;
    chatLi.querySelector('p').textContent = message;
    return chatLi;
}

// gera a resposta do gemini
const inputInitHeight = chatInput.scrollHeight;
const generateResponse = (incomingChatLi) => {
    const API_URL = "https://api.openai.com/v1/chat/completions";
    const messageElement = incomingChatLi.querySelector("p")

    const requestOptions = {
        method: "POST", 
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${API_KEY}`
        },
        body : JSON.stringify({
            model: "gemini-2.0-flash",
            messages: [{role: "user", content: UserMessage}]
        })
    }

    // tras a mensagem gerada e informa uma mensagem caso algo dê errado
    fetch(API_URL, requestOptions).then(res => res.json()).then(data => {
        messageElement.textContent = data.choices[0].message.content;
    }).catch((error) => {
        messageElement.textContent = "Opa, parece que algo deu errado. Por favor, tente novamente !";
    }).finally(() => chatbox.scrollTo(0, chatbox.scrollHeight));
}

// envia a mensagem digitada com a classe outgoing do css 
// adiciona a mensagem pensando enquanto o chat cria a mensagem
// usa a constante createChatLi para adicionar o texto digitado no Li

const handleChat = () => {
    UserMessage = chatInput.value.trim();
    chatInput.value = "";
    if(!UserMessage) return;
    chatbox.appendChild(createChatLi(UserMessage, "outgoing"));
    chatbox.scrollTo(0, chatbox.scrollHeight);
    setTimeout(() => {
        const incomingChatLi = createChatLi("Pensando...", "incoming")
        chatbox.appendChild(incomingChatLi);
        generateResponse(incomingChatLi);
        chatbox.scrollTo(0, chatbox.scrollHeight);
    },600);
}



// btn que envia a mensagem da constante handleChat
sendChatBtn.addEventListener("click", handleChat);

//enviar a mensagem com enter
chatInput.addEventListener("keydown", (event) => {
    if (event.key === "Enter" && !event.shiftKey) { 
        event.preventDefault();
        handleChat();
    }
});

chatInput.addEventListener("input", () => {
    
    chatInput.style.height = `${inputInitHeight}px`
    chatInput.style.height = `${chatInput.scrollHeight}px`
});