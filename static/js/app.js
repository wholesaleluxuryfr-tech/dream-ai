const messagesDiv = document.getElementById('chat-messages');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');
const girlId = messagesDiv ? messagesDiv.dataset.girlId : null;

let messageHistory = [];

function addMessage(role, content) {
    if (!messagesDiv) return;
    
    const msgObj = { role, content };
    messageHistory.push(msgObj);
    
    const div = document.createElement('div');
    div.classList.add('message', role === 'user' ? 'user' : 'ai');
    
    // Check for photo tag
    if (content.includes('[PHOTO:')) {
        const photoMatch = content.match(/\[PHOTO:(.*?)\]/);
        const photoDesc = photoMatch[1];
        const visibleText = content.replace(/\[PHOTO:.*?\]/, '').trim();
        
        div.innerText = visibleText;
        if (visibleText) {
            messagesDiv.appendChild(div);
        }
        
        const photoContainer = document.createElement('div');
        photoContainer.classList.add('message', 'ai');
        generatePhoto(photoDesc, photoContainer);
        messagesDiv.appendChild(photoContainer);
    } else {
        div.innerText = content;
        messagesDiv.appendChild(div);
    }
    
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

async function sendMessage() {
    const text = userInput.value.trim();
    if (!text) return;
    
    userInput.value = '';
    addMessage('user', text);
    
    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                girl_id: girlId,
                messages: messageHistory 
            })
        });
        
        if (!response.ok) throw new Error('Network error');
        
        const aiText = await response.text();
        addMessage('assistant', aiText);
    } catch (e) {
        console.error(e);
        const errorDiv = document.createElement('div');
        errorDiv.classList.add('message', 'ai');
        errorDiv.innerText = "Désolée, j'ai un souci technique. On reprend plus tard ?";
        messagesDiv.appendChild(errorDiv);
    }
}

async function generatePhoto(description, targetDiv) {
    const spinner = document.createElement('div');
    spinner.classList.add('loading-spinner');
    spinner.innerText = "En train de prendre une photo...";
    targetDiv.appendChild(spinner);

    try {
        const response = await fetch('/photo', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                girl_id: girlId,
                prompt: description
            })
        });
        
        const data = await response.json();
        const url = data.url || (data.data && data.data[0] && data.data[0].url);
        
        if (url) {
            const img = document.createElement('img');
            img.src = url;
            img.classList.add('photo-msg');
            img.onload = () => {
                messagesDiv.scrollTop = messagesDiv.scrollHeight;
            };
            targetDiv.appendChild(img);
        } else {
            targetDiv.innerText += " (Image non disponible)";
        }
    } catch (e) {
        console.error("Photo generation failed", e);
    } finally {
        spinner.remove();
    }
}

if (sendBtn) {
    sendBtn.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });
    
    // Initial greeting
    const greetings = {
        "anastasia": "Tu as une minute ? J'espère que c'est important.",
        "yuki": "Coucou... je suis en train de peindre, mais je voulais te dire bonjour.",
        "sofia": "Hola ! Prêt à danser avec moi ce soir ?"
    };
    setTimeout(() => {
        addMessage('assistant', greetings[girlId] || "Salut ! On discute ?");
    }, 500);
}
