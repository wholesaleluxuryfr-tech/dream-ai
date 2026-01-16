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
        const photoMatch = content.match(/\[PHOTO:(.*?)\]/);
        const photoDesc = photoMatch[1];
        
        // Remove the tag from visible text
        const visibleText = content.replace(/\[PHOTO:.*?\]/, '').trim();
        div.innerText = visibleText;
        
        // Call photo endpoint
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
        
        if (!response.ok) throw new Error('Network response was not ok');
        
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
    loading.style.marginTop = '10px';
    targetDiv.appendChild(loading);

    try {
        const response = await fetch('/photo', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                prompt: `a beautiful sexy 35yo Russian woman, CEO, ${description}, seductive look, cinematic lighting, high quality`,
                style: "cinematic",
                pose: "standing"
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
addMessage('assistant', "Salut... J'espère que tu as une bonne raison de me déranger.");
