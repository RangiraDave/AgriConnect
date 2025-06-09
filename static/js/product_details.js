document.addEventListener('DOMContentLoaded', function() {
    initializeChatbot();
    initializeImageGallery();
    initializeLocationMap();
});

function initializeChatbot() {
    const talkToUsButton = document.getElementById('talk-to-us');
    if (!talkToUsButton) return;

    talkToUsButton.addEventListener('click', function() {
        const chatbot = document.getElementById('chatbot');
        chatbot.style.display = 'block';
        const chatBody = chatbot.querySelector('.chatbot-body');
        chatBody.innerHTML = '';
        
        const userName = document.querySelector('meta[name="username"]')?.content || 'Guest';
        const productName = document.querySelector('meta[name="product-name"]')?.content || 'this product';
        
        const welcomeMessage = `Hello ${userName}, thank you for choosing ${productName}. I am LEA. How may I assist you?`;
        const botMessage = document.createElement('div');
        botMessage.className = 'message bot-message';
        botMessage.innerHTML = welcomeMessage;
        chatBody.appendChild(botMessage);
        chatBody.scrollTop = chatBody.scrollHeight;

        // Focus on input after opening
        setTimeout(() => {
            document.getElementById('chatbot-input').focus();
        }, 100);
    });

    // Handle Enter key in chat input
    const chatInput = document.getElementById('chatbot-input');
    if (chatInput) {
        chatInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                sendMessage();
            }
        });
    }
}

function sendMessage() {
    const input = document.getElementById('chatbot-input');
    const message = input.value.trim();
    const productId = document.querySelector('meta[name="product-id"]')?.content;
    const sessionId = document.getElementById('chatbot').getAttribute('data-session-id') || '';
    
    if (!message || !productId) return;

    const chatBody = document.querySelector('.chatbot-body');
    
    // Add user message
    const userMessage = document.createElement('div');
    userMessage.className = 'message user-message';
    userMessage.textContent = message;
    chatBody.appendChild(userMessage);
    
    // Clear input and scroll
    input.value = '';
    chatBody.scrollTop = chatBody.scrollHeight;

    // Show typing indicator
    const typingIndicator = document.createElement('div');
    typingIndicator.className = 'message bot-message typing-indicator';
    typingIndicator.innerHTML = '<span></span><span></span><span></span>';
    chatBody.appendChild(typingIndicator);
    chatBody.scrollTop = chatBody.scrollHeight;

    // Send message to server
    fetch(`/chatbot/get_response/?message=${encodeURIComponent(message)}&product_id=${productId}&session_id=${encodeURIComponent(sessionId)}`)
        .then(response => response.json())
        .then(data => {
            // Remove typing indicator
            typingIndicator.remove();
            
            // Store session ID
            document.getElementById('chatbot').setAttribute('data-session-id', data.session_id || '');
            
            // Add bot response
            const botMessage = document.createElement('div');
            botMessage.className = 'message bot-message';
            botMessage.innerHTML = data.response;
            chatBody.appendChild(botMessage);
            chatBody.scrollTop = chatBody.scrollHeight;
        })
        .catch(error => {
            console.error('Error:', error);
            typingIndicator.remove();
            
            const errorMessage = document.createElement('div');
            errorMessage.className = 'message bot-message error';
            errorMessage.textContent = "I'm sorry, I couldn't process your request. Please try again.";
            chatBody.appendChild(errorMessage);
            chatBody.scrollTop = chatBody.scrollHeight;
        });
}

function closeChatbot() {
    const chatbot = document.getElementById('chatbot');
    chatbot.style.display = 'none';
    chatbot.querySelector('.chatbot-body').innerHTML = '';
    document.getElementById('chatbot-input').value = '';
}

function initializeImageGallery() {
    const productMedia = document.querySelector('.product-media');
    if (!productMedia) return;

    // Add touch swipe support for mobile
    let touchStartX = 0;
    let touchEndX = 0;

    productMedia.addEventListener('touchstart', e => {
        touchStartX = e.changedTouches[0].screenX;
    }, false);

    productMedia.addEventListener('touchend', e => {
        touchEndX = e.changedTouches[0].screenX;
        handleSwipe();
    }, false);

    function handleSwipe() {
        const swipeThreshold = 50;
        if (touchEndX < touchStartX - swipeThreshold) {
            // Swipe left
            console.log('Swipe left');
        }
        if (touchEndX > touchStartX + swipeThreshold) {
            // Swipe right
            console.log('Swipe right');
        }
    }
}

function initializeLocationMap() {
    const locationLink = document.querySelector('a[href*="maps.google.com"]');
    if (!locationLink) return;

    // Add click tracking
    locationLink.addEventListener('click', function(e) {
        // You can add analytics tracking here
        console.log('Location map opened');
    });
}

// Handle mobile viewport height issues
function setViewportHeight() {
    let vh = window.innerHeight * 0.01;
    document.documentElement.style.setProperty('--vh', `${vh}px`);
}

window.addEventListener('resize', setViewportHeight);
setViewportHeight();

// Handle mobile keyboard
window.addEventListener('resize', function() {
    if (document.activeElement.tagName === 'INPUT') {
        window.scrollTo(0, 0);
    }
}); 