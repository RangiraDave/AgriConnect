// Chatbot Functionality
function initChatbot() {
    // Chatbot button click handler
    document.querySelectorAll('.chatbot-button').forEach(button => {
        button.addEventListener('click', function() {
            const productId = this.getAttribute('data-product-id');
            console.log('Chatbot button clicked for product:', productId);
            openChatbot(productId);
        });
    });

    // Chatbot message sending
    const chatbotInput = document.getElementById('chatbot-input');
    if (chatbotInput) {
        chatbotInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                sendMessage();
            }
        });
    } else {
        console.warn('Chatbot input not found in DOM');
    }
}

function openChatbot(productId) {
    const chatbot = document.getElementById('chatbot');
    if (!chatbot) {
        console.error('Chatbot modal not found in DOM');
        return;
    }
    chatbot.style.display = 'block';
    chatbot.setAttribute('data-product-id', productId);
    
    // Get product details for the title
    const productCard = document.querySelector(`.product-card[data-product-id="${productId}"]`);
    const productName = productCard ? productCard.querySelector('.card-title').textContent : 'Product';
    const productOwner = productCard ? productCard.querySelector('.owner-info small').textContent.split('-')[1].trim() : '';
    
    // Update chatbot title with product info
    const chatbotTitle = document.getElementById('chatbot-title');
    if (chatbotTitle) {
        chatbotTitle.textContent = productOwner ? `${productName} - ${productOwner}` : productName;
    }
    
    // Clear previous messages
    const chatBody = chatbot.querySelector('.chatbot-body');
    if (chatBody) {
        chatBody.innerHTML = '';
        // Add welcome message
        const welcomeMessage = document.createElement('div');
        welcomeMessage.className = 'message bot-message';
        welcomeMessage.textContent = `Hello! How can I help you with ${productName}?`;
        chatBody.appendChild(welcomeMessage);
    }
    console.log('Chatbot modal opened for product:', productId);
}

function closeChatbot() {
    const chatbot = document.getElementById('chatbot');
    if (!chatbot) return;
    chatbot.style.display = 'none';
    const chatBody = chatbot.querySelector('.chatbot-body');
    if (chatBody) chatBody.innerHTML = '';
    const chatbotInput = document.getElementById('chatbot-input');
    if (chatbotInput) chatbotInput.value = '';
}

function sendMessage() {
    const input = document.getElementById('chatbot-input');
    if (!input) return;
    const message = input.value.trim();
    const chatbot = document.getElementById('chatbot');
    const productId = chatbot ? chatbot.getAttribute('data-product-id') : '';
    const sessionId = chatbot ? chatbot.getAttribute('data-session-id') || '' : '';

    if (message) {
        const chatBody = document.querySelector('.chatbot-body');
        if (!chatBody) return;
        // Add user message
        const userMessage = document.createElement('div');
        userMessage.className = 'message user-message';
        userMessage.textContent = message;
        chatBody.appendChild(userMessage);
        // Clear input
        input.value = '';
        // Send message to server
        fetch(`/chatbot/get_response/?message=${encodeURIComponent(message)}&product_id=${encodeURIComponent(productId)}&session_id=${encodeURIComponent(sessionId)}`)
            .then(response => response.json())
            .then(data => {
                // Store session ID for conversation continuity
                if (chatbot) chatbot.setAttribute('data-session-id', data.session_id || '');
                const botMessage = document.createElement('div');
                botMessage.className = 'message bot-message';
                botMessage.textContent = data.response;
                chatBody.appendChild(botMessage);
                chatBody.scrollTop = chatBody.scrollHeight;
            })
            .catch(error => {
                console.error('Error:', error);
                if (typeof showToast === 'function') showToast('Error sending message');
            });
    }
}
