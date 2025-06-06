// Chatbot Functionality
function initChatbot() {
    // Chatbot button click handler
    document.querySelectorAll('.chatbot-button').forEach(button => {
        button.addEventListener('click', function() {
            const productId = this.getAttribute('data-product-id');
            openChatbot(productId);
        });
    });

    // Chatbot message sending
    document.getElementById('chatbot-input').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            sendMessage();
        }
    });
}

function openChatbot(productId) {
    const chatbot = document.getElementById('chatbot');
    chatbot.style.display = 'block';
    chatbot.setAttribute('data-product-id', productId);
    
    // Get product details for the title
    const productCard = document.querySelector(`.product-card[data-product-id="${productId}"]`);
    const productName = productCard ? productCard.querySelector('.card-title').textContent : 'Product';
    const productOwner = productCard ? productCard.querySelector('.owner-info small').textContent.split('-')[1].trim() : '';
    
    // Update chatbot title with product info
    const chatbotTitle = document.getElementById('chatbot-title');
    chatbotTitle.textContent = productOwner ? `${productName} - ${productOwner}` : productName;
    
    // Clear previous messages
    const chatBody = chatbot.querySelector('.chatbot-body');
    chatBody.innerHTML = '';
    
    // Add welcome message
    const welcomeMessage = document.createElement('div');
    welcomeMessage.className = 'message bot-message';
    welcomeMessage.textContent = `Hello! How can I help you with ${productName}?`;
    chatBody.appendChild(welcomeMessage);
}

function closeChatbot() {
    const chatbot = document.getElementById('chatbot');
    chatbot.style.display = 'none';
    chatbot.querySelector('.chatbot-body').innerHTML = '';
    document.getElementById('chatbot-input').value = '';
}

function sendMessage() {
    const input = document.getElementById('chatbot-input');
    const message = input.value.trim();
    const productId = document.getElementById('chatbot').getAttribute('data-product-id');
    const sessionId = document.getElementById('chatbot').getAttribute('data-session-id') || '';

    if (message) {
        const chatBody = document.querySelector('.chatbot-body');
        
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
                document.getElementById('chatbot').setAttribute('data-session-id', data.session_id || '');
                
                const botMessage = document.createElement('div');
                botMessage.className = 'message bot-message';
                botMessage.textContent = data.response;
                chatBody.appendChild(botMessage);
                chatBody.scrollTop = chatBody.scrollHeight;
            })
            .catch(error => {
                console.error('Error:', error);
                showToast('Error sending message');
            });
    }
}
