document.addEventListener('DOMContentLoaded', () => {
    const chatContainer = document.getElementById('chatMessages');
    const userMessageInput = document.getElementById('userMessage');
    const sendMessageButton = document.getElementById('sendMessage');

    function addMessage(message, type) {
        const messageElement = document.createElement('div');
        messageElement.classList.add(type + '-message');
        messageElement.textContent = message;
        chatContainer.appendChild(messageElement);
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    function sendMessage() {
        const userMessage = userMessageInput.value.trim();
        if (!userMessage) return;

        // Add user message to chat
        addMessage(userMessage, 'user');
        userMessageInput.value = '';

        // Send message to backend
        fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: userMessage })
        })
        .then(response => response.json())
        .then(data => {
            // Add AI response to chat
            addMessage(data.message, 'ai');
        })
        .catch(error => {
            console.error('Error:', error);
            addMessage('Sorry, I am having trouble responding right now.', 'ai');
        });
    }

    // Send message on button click
    sendMessageButton.addEventListener('click', sendMessage);

    // Send message on Enter key press
    userMessageInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
});
