let chatHistory = [];
let isLoading = false;

function addMessage(message, isUser = false) {
    const messagesDiv = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
    messageDiv.textContent = message;
    messagesDiv.appendChild(messageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;

    // Add message to chat history
    chatHistory.push({
        role: isUser ? 'Human' : 'AI',
        content: message
    });
}

function showLoadingIndicator() {
    const messagesDiv = document.getElementById('chat-messages');
    const template = document.getElementById('loading-template');
    const loading = template.content.cloneNode(true);
    messagesDiv.appendChild(loading);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

function removeLoadingIndicator() {
    const loadingMessage = document.querySelector('.loading-message');
    if (loadingMessage) {
        loadingMessage.remove();
    }
}

function setLoading(loading) {
    isLoading = loading;
    const button = document.getElementById('send-button');
    const input = document.getElementById('user-input');
    
    button.disabled = loading;
    input.disabled = loading;
    
    if (loading) {
        showLoadingIndicator();
    } else {
        removeLoadingIndicator();
    }
}

async function sendMessage() {
    const input = document.getElementById('user-input');
    const message = input.value.trim();
    
    if (!message || isLoading) return;
    
    addMessage(message, true);
    input.value = '';
    
    setLoading(true);

    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 
                message: message,
                chat_history: chatHistory
            })
        });
        
        const data = await response.json();
        
        setLoading(false);
        
        if (data.error) {
            addMessage('Sorry, an error occurred. Please try again.');
            return;
        }
        
        addMessage(data.response);
    } catch (error) {
        console.error('Error:', error);
        setLoading(false);
        addMessage('Sorry, an error occurred. Please try again.');
    }
}

// Get initial message from the server
window.onload = async function() {
    setLoading(true);
    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 
                message: 'start',
                chat_history: []
            })
        });
        
        const data = await response.json();
        setLoading(false);
        if (!data.error) {
            addMessage(data.response);
        }
    } catch (error) {
        console.error('Error:', error);
        setLoading(false);
        addMessage('Hello! How can I assist you today?');
    }
};

// Handle enter key press
document.getElementById('user-input').addEventListener('keypress', function(e) {
    if (e.key === 'Enter' && !isLoading) {
        sendMessage();
    }
});

function formatMessage(text) {
    // Handle bold text (text between **)
    text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    
    // Handle line breaks
    text = text.replace(/\n/g, '<br>');
    
    return text;
}

function addMessage(message, isUser = false) {
    const messagesDiv = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
    
    // Use innerHTML instead of textContent to render HTML formatting
    messageDiv.innerHTML = formatMessage(message);
    
    messagesDiv.appendChild(messageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;

    // Add message to chat history (store original message with formatting)
    chatHistory.push({
        role: isUser ? 'Human' : 'AI',
        content: message
    });
}