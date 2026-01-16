const messagesDiv = document.getElementById('chat-messages');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');

let messageHistory = [];

function addMessage(role, content) {
    const msgObj = { role, content };
    messageHistory.push(msgObj);
    
    const div = document.createElement('div');
    div.classList.add('message', role === 'user' ? 'user' : 'ai');
    
    // Check for photo tag
    if (content.includes('[PHOTO:')) {
        const parts = content.split(/\[PHOTO:.*?\]/);
        div.innerText = parts.join(' ').trim();
        
        const photoDesc = content.match(/\[PHOTO:(.*?)\]/)[1];
        generatePhoto(photoDesc, div);
    } else {
        div.innerText = content;
    }
    
    messagesDiv.appendChild(div);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

async function sendMessage() {
    const text = userInput.value.trim();
    if (!text) return;
    
    userInput.value = '';
    addMessage('user', text);
    
    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ messages: messageHistory })
        });
        
        const aiText = await response.text();
        addMessage('assistant', aiText);
    } catch (e) {
        console.error(e);
        addMessage('assistant', "Désolée, j'ai un petit problème technique.");
    }
}

async function generatePhoto(description, targetDiv) {
    const loading = document.createElement('p');
    loading.innerText = "...en train de prendre une photo...";
    loading.style.fontSize = '0.8rem';
    loading.style.fontStyle = 'italic';
    targetDiv.appendChild(loading);

    try {
        const response = await fetch('/photo', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                prompt: `a beautiful 35yo Russian woman, CEO, ${description}, cinematic lighting, high quality`,
                style: "cinematic",
                pose: "standing"
            })
        });
        
        const data = await response.json();
        if (data.url || (data.data && data.data[0] && data.data[0].url)) {
            const url = data.url || data.data[0].url;
            const img = document.createElement('img');
            img.src = url;
            img.classList.add('photo-msg');
            targetDiv.appendChild(img);
        }
    } catch (e) {
        console.error("Photo generation failed", e);
    } finally {
        loading.remove();
    }
}

sendBtn.addEventListener('click', sendMessage);
userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
});

// Initial message
addMessage('assistant', "Bonjour. Je suis Anastasia. Que voulez-vous ?");
