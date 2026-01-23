document.addEventListener('DOMContentLoaded', () => {
    // Inject HTML Structure
    const chatWidget = document.createElement('div');
    chatWidget.innerHTML = `
        <div class="chatbot-trigger" id="chatbotTrigger">
            <i class="bi bi-chat-dots-fill"></i>
        </div>
        <div class="chat-window" id="chatWindow">
            <div class="chat-header">
                <div class="d-flex align-items-center gap-2">
                    <i class="bi bi-robot"></i>
                    <h5 data-i18n="chat_header">EMS Assistant</h5>
                </div>
                <button class="chat-close" id="chatClose">
                    <i class="bi bi-x-lg"></i>
                </button>
            </div>
            <div class="chat-body" id="chatBody">
                <div class="message bot" data-i18n="chat_greeting">
                    Hello! I'm your EMS AI Assistant. I can help you find events, answer payment questions, or guide you through booking. How can I help today?
                </div>
                <div class="typing-indicator" id="typingIndicator">
                    <span></span><span></span><span></span>
                </div>
            </div>
            <div class="chat-footer">
                <input type="text" class="chat-input" id="chatInput" data-i18n="chat_placeholder" placeholder="Type a message...">
                <button class="chat-send" id="chatSend">
                    <i class="bi bi-send-fill"></i>
                </button>
            </div>
        </div>
    `;
    document.body.appendChild(chatWidget);

    // Elements
    const trigger = document.getElementById('chatbotTrigger');
    const window = document.getElementById('chatWindow');
    const closeBtn = document.getElementById('chatClose');
    const input = document.getElementById('chatInput');
    const sendBtn = document.getElementById('chatSend');
    const body = document.getElementById('chatBody');
    const typing = document.getElementById('typingIndicator');

    // State
    let isOpen = false;
    const API_URL = (typeof API_BASE_URL !== 'undefined' ? API_BASE_URL : 'http://127.0.0.1:8000') + '/ai/chat';

    // Toggle Window
    function toggleChat() {
        isOpen = !isOpen;
        if (isOpen) {
            window.classList.add('active');
            input.focus();
        } else {
            window.classList.remove('active');
        }
    }

    trigger.addEventListener('click', toggleChat);
    closeBtn.addEventListener('click', toggleChat);

    // Send Message
    async function sendMessage() {
        const message = input.value.trim();
        if (!message) return;

        // Add User Message
        appendMessage(message, 'user');
        input.value = '';

        // Show Typing
        typing.style.display = 'block';
        body.scrollTop = body.scrollHeight;

        try {
            const response = await fetch(API_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    message: message,
                    lang: localStorage.getItem('preferredLanguage') || 'en'
                })
            });

            const data = await response.json();

            // Hide Typing
            typing.style.display = 'none';

            if (data.response) {
                appendMessage(data.response, 'bot');
            } else {
                appendMessage("Sorry, I encountered an error.", 'bot');
            }

        } catch (error) {
            console.error('Chat Error:', error);
            typing.style.display = 'none';
            appendMessage("Offline mode: Unable to connect to AI server.", 'bot');
        }
    }

    function appendMessage(text, type) {
        const div = document.createElement('div');
        div.className = `message ${type}`;
        div.textContent = text;
        body.insertBefore(div, typing); // Insert before typing indicator
        body.scrollTop = body.scrollHeight;
    }

    // Event Listeners
    sendBtn.addEventListener('click', sendMessage);
    input.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });
});
