# chatbot/views.py
import json
import re
import logging
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from core.models import Product, ChatLog

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
    ],
    'help_request': [
        r'\b(?:help|assist|guide)\b',
        r'\bwhat can you (?:do|help|assist)\b',
        r'\bhow (?:can|do) you (?:help|assist|work)\b',
        r'\bwhat (?:should|can) I ask\b',
        r'\bwhat questions\b',
    ],
}

def detect_intent(message):
    """Determine the intent of the user's message"""
    message = message.lower().strip()
    
    # Check each pattern category
    for intent, pattern_list in PATTERNS.items():
        for pattern in pattern_list:
            if re.search(pattern, message):
                logger.info(f"Message '{message}' matched pattern '{pattern}' with intent '{intent}'")
                return intent
    
    # Very short messages (1-2 words) might be greetings or simple queries
    words = message.strip().split()
    if len(words) <= 2:
        if any(greeting in words for greeting in ['hi', 'hello', 'hey', 'hola']):
            return 'greeting'
        if any(word in words for word in ['price', 'cost', 'contact', 'call', 'help']):
            for word in words:
                if word == 'price' or word == 'cost':
                    return 'price_inquiry'
                elif word == 'contact' or word == 'call':
                    return 'contact_request'
                elif word == 'help':
                    return 'help_request'
    
    # Default fallback
    logger.info(f"No intent matched for message: '{message}'")
    return 'unknown'

def get_product_info(product_id):
    """Get formatted product information"""
    try:
        product = get_object_or_404(Product, id=product_id)
        
        # Get contact information from product owner
        contact = None
        # Try direct contact field (if it exists)
        if hasattr(product, 'contact') and getattr(product, 'contact', None):
            contact = product.contact
        # Try profile phone
        elif hasattr(product.owner, 'profile'):
            contact = getattr(product.owner.profile, 'phone', None)
        # If still no contact, try other profile fields
        if not contact and hasattr(product.owner, 'profile'):
            profile = product.owner.profile
            contact = getattr(profile, 'contact_number', None) or getattr(profile, 'email', None)
        
        # Format contact if found, otherwise provide guidance
        if contact:
            formatted_contact = contact
        else:
            formatted_contact = "Contact information not available. Please check seller profile."
        
        # Prepare product information
        product_info = {
            'name': product.name,
            'description': product.description or "No description available",
            'price': product.price_per_unit,
            'unit': product.unit,
            'quantity': product.quantity_available,
            'contact': formatted_contact,
            'owner': product.owner.username,
        }
        
        logger.info(f"Successfully retrieved product info for product ID: {product_id}")
        return product_info
    except Product.DoesNotExist:
        logger.error(f"Product with ID {product_id} not found")
        return None
    except Exception as e:
        logger.error(f"Error retrieving product info for ID {product_id}: {str(e)}")
        return None

def generate_response(intent, product_info):
    """Generate a response based on intent and product information"""
    if not product_info:
        return "I'm sorry, I couldn't find information about this product."
    
    product_name = product_info.get('name', 'this product')
    
    owner_name = product_info.get('owner', 'the seller')
    responses = {
        'greeting': f"Hello! I can help you with information about {product_name}. What would you like to know?",
        
        'product_info': f"{product_name}: {product_info['description']} It costs {product_info['price']} per {product_info['unit']} and there are {product_info['quantity']} {product_info['unit']}s available. The seller is {owner_name}.",
        
        'price_inquiry': f"The price of '{product_name}' is {product_info['price']} per {product_info['unit']}.",
        
        'contact_request': f"You can contact the {owner_name} at {product_info['contact']}.",
        
        'availability': f"There are currently {product_info['quantity']} {product_info['unit']}s of '{product_name}' available.",
        
        'location_inquiry': f"For location details and delivery options for {product_name}, please contact the seller {owner_name} directly at {product_info['contact']}.",
        
        'help_request': f"I can answer questions about {product_name} including:\n• Product details and description\n• Price ({product_info['price']} per {product_info['unit']})\n• Availability ({product_info['quantity']} {product_info['unit']}s)\n• How to contact the seller ({owner_name})\nJust ask what you'd like to know!",
        
        'unknown': f"I'm not sure what you're asking about {product_name}. You can ask about the product details, price, availability, or how to contact the seller {owner_name}."
    }
    
    return responses.get(intent, responses['unknown'])

def log_conversation(user_message, bot_response, intent, product_id):
    """Log the conversation to the database"""
    try:
        ChatLog.objects.create(
            user_message=user_message,
            bot_response=bot_response,
            intent=intent,
            product_id=product_id
        )
    except Exception as e:
        logger.error(f"Failed to log conversation: {str(e)}")

def chatbot_response(request):
    """Process chatbot requests and return responses"""
    message = request.GET.get('message', '').strip()
    product_id = request.GET.get('product_id')
    
    if not message or not product_id:
        return JsonResponse({
            'response': "I'm sorry, I couldn't process your request."
        })
    
    try:
        # Get product information
        product_info = get_product_info(product_id)
        
        if not product_info:
            return JsonResponse({
                'response': "I'm sorry, I couldn't find information about this product."
            })
        
        # Determine intent from message
        intent = detect_intent(message)
        logger.info(f"Detected intent '{intent}' for message: '{message}'")
        
        # Generate appropriate response
        response = generate_response(intent, product_info)
        
        # Log the conversation
        log_conversation(message, response, intent, product_id)
        
        return JsonResponse({'response': response})
        
    except Exception as e:
        logger.error(f"Error in chatbot_response: {str(e)}")
        return JsonResponse({
            'response': "I'm sorry, there was an error processing your request."
        })
