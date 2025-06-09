# chatbot/views.py
import json
import re
import logging
import random
import uuid
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from core.models import Product
from django.core.cache import cache
from .ai_chatbot import chatbot as ai_chatbot
from django.utils.safestring import mark_safe

logger = logging.getLogger(__name__)

# Enhanced patterns for more accurate intent recognition
PATTERNS = {
    'greeting': [
        r'\b(?:hello|hi|hey|greetings|hola|bonjour)\b',
        r'\bhow are you\b',
        r'\bgood (?:morning|afternoon|evening|day)\b',
    ],
    'product_info': [
        r'\b(?:what|tell me|info|information|details|learn|know)\b.*\b(?:about|regarding|on)\b',
        r'\b(?:describe|explain|elaborate|details)\b',
        r'\bmore details\b',
        r'\bwhat (?:product|item) is this\b',
        r'\bwhat is (?:it|this)\b',
        r'\bwhat can you tell me\b',
        r'\bdescribe this product\b',
        r'\btell me about\b',
        r'\bproduct details\b',
    ],
    'price_inquiry': [
        r'\b(?:price|cost|how much)\b',
        r'\b(?:pricing|fee|charge|rate)\b',
        r'\bhow much (?:does|is|costs|will)\b',
        r'\bhow many (?:rwf|dollars)\b',
    ],
    'contact_request': [
        r'\b(?:contact|reach|call|phone|email|message|number)\b',
        r'\b(?:seller|vendor|owner|supplier|farmer)\b',
        r'\bhow (?:to|can|do) (?:contact|reach|call)\b',
        r'\bget in touch\b',
        r'\bphoning\b',
        r'\btalking to\b',
    ],
    'availability': [
        r'\b(?:available|in stock|quantity|how many)\b',
        r'\b(?:have|left|remain|stock)\b',
        r'\bhow much (?:is|are) available\b',
        r'\bquantity left\b',
        r'\bhow many units\b',
    ],
    'location_inquiry': [
        r'\b(?:where|location|address|place|area)\b',
        r'\bwhere (?:is|can|to)\b',
        r'\bpick up\b',
        r'\bdelivery\b',
        r'\b(?:find|locate|get to|reach|access)\b',
        r'\b(?:near|close|nearby|around|in the area)\b',
        r'\b(?:distance|how far|how close)\b',
        r'\b(?:map|directions|route|way)\b',
        r'\b(?:coordinates|gps|latitude|longitude)\b',
        r'\b(?:market|shop|store|seller|vendor)\b.*\b(?:location|place|where)\b',
        r'\b(?:pickup|collection|meeting)\b.*\b(?:point|place|location)\b',
        r'\b(?:transport|shipping|delivery)\b.*\b(?:options|available|possible)\b',
    ],
    'help_request': [
        r'\b(?:help|assist|guide)\b',
        r'\bwhat can you (?:do|help|assist)\b',
        r'\bhow (?:can|do) you (?:help|assist|work)\b',
        r'\bwhat (?:should|can) I ask\b',
        r'\bwhat questions\b',
    ],
}

# Store conversation history
CONVERSATION_TTL = 60 * 30  # 30 minutes

def get_conversation_key(product_id, session_id=None):
    """Generate a unique key for storing conversation history"""
    if session_id:
        return f"chat_history_{product_id}_{session_id}"
    return f"chat_history_{product_id}"

def get_conversation_history(product_id, session_id=None):
    """Retrieve conversation history from cache"""
    key = get_conversation_key(product_id, session_id)
    history = cache.get(key, [])
    return history

def save_conversation_history(product_id, history, session_id=None):
    """Save conversation history to cache"""
    key = get_conversation_key(product_id, session_id)
    cache.set(key, history, CONVERSATION_TTL)

def detect_intent(message, history=None):
    """Determine the intent of the user's message with context awareness."""
    message = message.lower().strip()
    
    # Special handling for follow-up messages based on history
    if history and len(history) > 1:
        last_bot_intent = history[-1].get('intent', 'unknown')
        
        # Check for conversational follow-ups
        if last_bot_intent == 'greeting' and re.search(r'\b(fine|good|great|well|okay|not bad)\b', message):
            return 'casual_conversation'
        
        # Check for price follow-up questions
        if last_bot_intent == 'price_inquiry' and re.search(r'\b(cheaper|expensive|discount|better price|negotiate)\b', message):
            return 'price_inquiry'
    
    # Check each pattern category
    for intent, pattern_list in PATTERNS.items():
        for pattern in pattern_list:
            if re.search(pattern, message):
                logger.info(f"Message '{message}' matched pattern '{pattern}' with intent '{intent}'")
                return intent
    
    # Handle ambiguous or irrelevant inputs
    if len(message.split()) <= 3 and not re.search(r'[a-zA-Z]', message):
        return 'irrelevant'
    if re.match(r'^[a-zA-Z]+$', message) and len(message) < 5:
        return 'irrelevant'
    
    # Default fallback
    logger.info(f"No intent matched for message: '{message}'")
    return 'unknown'

def get_product_info(product_id):
    """Get formatted product information with full context for AIChatbot"""
    try:
        # Use the AIChatbot's get_product_context to get all fields (including location)
        return ai_chatbot.get_product_context(product_id)
    except Exception as e:
        logger.error(f"Error retrieving product info for ID {product_id}: {str(e)}")
        return None

def generate_response(intent, product_info, message=None, history=None):
    """Generate a response based on intent, product information, and conversation history."""
    if not product_info:
        return "I'm sorry, I couldn't find information about this product."
    
    product_name = product_info.get('name', 'this product')
    owner_name = product_info.get('owner', 'the seller')
    
    try:
        # Use AI model for response generation
        ai_response = ai_chatbot.generate_response(
            message=message,
            product_context=product_info,
            session_id=str(uuid.uuid4())
        )
        if ai_response:
            return ai_response
    except Exception as e:
        logger.error(f"AI response generation failed: {str(e)}")
    
    # Fallback to rule-based responses
    responses = {
        'greeting': f"Hello! I can help you with information about {product_name}. What would you like to know?",
        'casual_conversation': "I'm just a chatbot here to assist you with product information. How can I help?",
        'irrelevant': "I'm sorry, I didn't understand that. Could you ask something specific about the product?",
        'unknown': f"I'm not sure I understand. Could you clarify your question about {product_name}?",
    }
    
    # Provide varied fallback responses for unknown intents
    if intent == 'unknown':
        fallback_responses = [
            f"I'm not sure I understand. Could you clarify your question about {product_name}?",
            f"Could you rephrase your question about {product_name}? I'd love to help.",
            f"Hmm, I didn't catch that. What would you like to know about {product_name}?",
        ]
        return random.choice(fallback_responses)
    
    return responses.get(intent, responses['unknown'])

def chatbot_response(request):
    """Process chatbot requests and return responses"""
    message = request.GET.get('message', '').strip()
    product_id = request.GET.get('product_id')
    session_id = request.GET.get('session_id', None) or request.session.session_key
    
    if not message or not product_id:
        return JsonResponse({
            'response': "I'm sorry, I couldn't process your request."
        })
    
    try:
        # Get conversation history
        history = get_conversation_history(product_id, session_id)
        
        # Get product information
        product_info = get_product_info(product_id)
        if product_info:
            product_info['id'] = product_id  # Add ID for AI context
        
        if not product_info:
            return JsonResponse({
                'response': "I'm sorry, I couldn't find information about this product."
            })
        
        # Determine intent from message with conversation context
        intent = detect_intent(message, history)
        logger.info(f"Detected intent '{intent}' for message: '{message}'")
        
        # Generate appropriate response with context
        response = generate_response(intent, product_info, message, history)
        
        # Mark the response as safe HTML
        safe_response = mark_safe(response)
        
        return JsonResponse({
            'response': safe_response,
            'session_id': session_id
        })
        
    except Exception as e:
        logger.error(f"Error in chatbot_response: {str(e)}")
        return JsonResponse({
            'response': "I'm sorry, there was an error processing your request."
        })
