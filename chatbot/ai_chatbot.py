from audioop import avg
import os
import logging
from typing import Dict, Tuple, Optional, List
import re
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
from core.models import Product, Profile, ChatLog
import requests
from urllib3.exceptions import InsecureRequestWarning
from django.db.models import Avg

# Disable SSL verification warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

logger = logging.getLogger(__name__)

class AIChatbot:
    def __init__(self):
        """Initialize the chatbot with a lightweight model."""
        self.model = None
        self.tokenizer = None
        self.model_loaded = False
        
        try:
            # Try to load the model with SSL verification disabled
            os.environ['CURL_CA_BUNDLE'] = ''
            from transformers import AutoModelForCausalLM, AutoTokenizer
            
            model_name = "microsoft/DialoGPT-small"
            self.tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
            self.tokenizer.pad_token = self.tokenizer.eos_token
            self.tokenizer.padding_side = 'left'
            
            self.model = AutoModelForCausalLM.from_pretrained(model_name, trust_remote_code=True)
            self.model.config.pad_token_id = self.tokenizer.pad_token_id
            self.model_loaded = True
            logger.info("Successfully loaded DialoGPT model")
        except Exception as e:
            logger.error(f"Failed to load model: {str(e)}")
            self.model_loaded = False

    def detect_intent(self, message: str) -> Tuple[str, float]:
        """Detect the intent of the user's message using regex patterns."""
        message = message.lower()
        
        # Define intent patterns
        patterns = {
            'greeting': r'\b(hi|hello|hey|greetings|good (morning|afternoon|evening))\b',
            'farewell': r'\b(bye|goodbye|see you|farewell)\b',
            'product_info': r'\b(product|item|price|cost|available|quantity|stock|how much|how many|what is|what are)\b',
            'location': r'\b(where|location|address|place|find|near)\b',
            'contact': r'\b(contact|phone|number|email|reach|call)\b',
            'rating': r'\b(rating|review|star|feedback|rate)\b',
            'media': r'\b(picture|image|photo|video|media)\b',
            'help': r'\b(help|support|assist|how to|guide|what can)\b'
        }
        
        # Check each pattern
        for intent, pattern in patterns.items():
            if re.search(pattern, message):
                return intent, 0.8  # High confidence for regex matches
        
        # Check for follow-up questions
        if any(word in message for word in ['it', 'this', 'that', 'the', 'one']):
            return 'product_info', 0.7  # Medium confidence for follow-ups
        
        return 'unknown', 0.5  # Default intent with medium confidence

    def get_product_context(self, product_id: Optional[int] = None) -> Dict:
        """Get context about a product if product_id is provided."""
        if not product_id:
            return {}
            
        try:
            product = Product.objects.select_related(
                'owner__profile__farmer',
                'owner__profile__cooperative'
            ).get(id=product_id)
            
            # Get seller's location information
            location_info = {}
            if hasattr(product.owner.profile, 'farmer'):
                location = product.owner.profile.farmer
                location_info = {
                    'province': location.province.name if location.province else 'N/A',
                    'district': location.district.name if location.district else 'N/A',
                    'sector': location.sector.name if location.sector else 'N/A',
                    'cell': location.cell.name if location.cell else 'N/A',
                    'village': location.village.name if location.village else 'N/A',
                    'specific_location': location.specific_location or 'N/A'
                }
            elif hasattr(product.owner.profile, 'cooperative'):
                location = product.owner.profile.cooperative
                location_info = {
                    'province': location.province.name if location.province else 'N/A',
                    'district': location.district.name if location.district else 'N/A',
                    'sector': location.sector.name if location.sector else 'N/A',
                    'cell': location.cell.name if location.cell else 'N/A',
                    'village': location.village.name if location.village else 'N/A',
                    'specific_location': location.specific_location or 'N/A'
                }
            
            # Format location string
            location_str = ""
            if location_info:
                location_parts = []
                for key in ['province', 'district', 'sector', 'cell', 'village']:
                    if location_info[key] != 'N/A':
                        location_parts.append(location_info[key])
                if location_info['specific_location'] != 'N/A':
                    location_parts.append(f"({location_info['specific_location']})")
                location_str = ", ".join(location_parts) if location_parts else "Location not specified"
            
            return {
                'name': product.name,
                'description': product.description,
                'price': product.price_per_unit,
                'quantity': product.quantity_available,
                'unit': product.unit,
                'seller': product.owner.username,
                'rating': product.ratings.aggregate(Avg('rating'))['rating__avg'] or 0,
                'location': location_str,
                'contact': product.contact or product.owner.profile.phone or 'N/A',
                'created_at': product.created_at.strftime("%B %d, %Y"),
                'media': bool(product.media)
            }
        except Product.DoesNotExist:
            return {}

    def process_intent(self, message: str) -> Tuple[str, Dict]:
        """Process the user's message to determine intent and required information."""
        try:
            # First try regex-based intent detection
            intent, confidence = self.detect_intent(message)
            
            # Determine what information is needed based on the message
            info_needed = []
            message_lower = message.lower()
            
            if 'price' in message_lower or 'cost' in message_lower or 'how much' in message_lower:
                info_needed.extend(['name', 'price', 'unit'])
            elif 'quantity' in message_lower or 'available' in message_lower or 'stock' in message_lower:
                info_needed.extend(['name', 'quantity', 'unit'])
            elif 'location' in message_lower or 'where' in message_lower:
                info_needed.extend(['name', 'location'])
            elif 'contact' in message_lower or 'phone' in message_lower or 'number' in message_lower:
                info_needed.extend(['name', 'contact'])
            elif 'rating' in message_lower or 'review' in message_lower:
                info_needed.extend(['name', 'rating'])
            elif 'name' in message_lower or 'what is' in message_lower:
                info_needed.extend(['name', 'description'])
            elif 'help' in message_lower or 'what can' in message_lower:
                info_needed = ['name']  # Just get the name for context
            elif intent in ['greeting', 'farewell']:
                info_needed = ['name']  # Just get the name for context
            
            # Determine if it's a follow-up question
            is_followup = any(word in message_lower for word in ['it', 'this', 'that', 'the', 'one'])
            
            return intent, {
                'info_needed': info_needed,
                'is_followup': is_followup
            }
            
        except Exception as e:
            logger.error(f"Error in process_intent: {str(e)}")
            return 'unknown', {'info_needed': [], 'is_followup': False}

    def get_targeted_product_info(self, product_id: Optional[int], info_needed: List[str]) -> Dict:
        """Get only the requested product information from the database."""
        if not product_id or not info_needed:
            return {}
            
        try:
            product = Product.objects.select_related(
                'owner__profile__farmer',
                'owner__profile__cooperative'
            ).get(id=product_id)
            
            result = {}
            
            # Basic product info
            if any(i in ['name', 'description', 'price', 'quantity', 'unit'] for i in info_needed):
                result.update({
                    'name': product.name,
                    'description': product.description,
                    'price': product.price_per_unit,
                    'quantity': product.quantity_available,
                    'unit': product.unit
                })
            
            # Location info
            if 'location' in info_needed:
                location_info = {}
                if hasattr(product.owner.profile, 'farmer'):
                    location = product.owner.profile.farmer
                    location_info = {
                        'province': location.province.name if location.province else 'N/A',
                        'district': location.district.name if location.district else 'N/A',
                        'sector': location.sector.name if location.sector else 'N/A',
                        'cell': location.cell.name if location.cell else 'N/A',
                        'village': location.village.name if location.village else 'N/A',
                        'specific_location': location.specific_location or 'N/A'
                    }
                elif hasattr(product.owner.profile, 'cooperative'):
                    location = product.owner.profile.cooperative
                    location_info = {
                        'province': location.province.name if location.province else 'N/A',
                        'district': location.district.name if location.district else 'N/A',
                        'sector': location.sector.name if location.sector else 'N/A',
                        'cell': location.cell.name if location.cell else 'N/A',
                        'village': location.village.name if location.village else 'N/A',
                        'specific_location': location.specific_location or 'N/A'
                    }
                
                # Format location string
                location_parts = []
                for key in ['province', 'district', 'sector', 'cell', 'village']:
                    if location_info.get(key, 'N/A') != 'N/A':
                        location_parts.append(location_info[key])
                if location_info.get('specific_location', 'N/A') != 'N/A':
                    location_parts.append(f"({location_info['specific_location']})")
                result['location'] = ", ".join(location_parts) if location_parts else "Location not specified"
            
            # Contact info
            if 'contact' in info_needed:
                result['contact'] = product.contact or product.owner.profile.phone or 'N/A'
            
            # Rating info
            if 'rating' in info_needed:
                result['rating'] = product.ratings.aggregate(Avg('rating'))['rating__avg'] or 0
            
            # Media info
            if 'media' in info_needed:
                result['media'] = bool(product.media)
            
            # Seller info
            if 'seller' in info_needed:
                result['seller'] = product.owner.username
            
            return result
            
        except Product.DoesNotExist:
            return {}

    def generate_response(self, message: str, product_id: Optional[int] = None, session_id: Optional[str] = None) -> str:
        """Generate a response based on the user's message."""
        try:
            # First, process the intent and determine what information is needed
            intent, analysis = self.process_intent(message)
            
            # Get only the required product information
            product_context = self.get_targeted_product_info(product_id, analysis['info_needed'])
            
            # For simple responses or when AI model is not available, use rule-based system
            if intent in ['greeting', 'farewell', 'help'] or len(message.split()) <= 2 or not self.model_loaded:
                return self._rule_based_response(intent, product_context)
            
            try:
                # Prepare context for response generation
                context = "You are a helpful product assistant for an agricultural marketplace. "
                if product_context:
                    context += "Here is the requested information:\n"
                    for key, value in product_context.items():
                        if value != 'N/A':  # Only include non-N/A values
                            context += f"- {key.title()}: {value}\n"
                
                # Add conversation context
                context += f"\nUser intent: {intent}\n"
                context += "Instructions: Provide a clear, concise response using the provided information. "
                if analysis['is_followup']:
                    context += "This is a follow-up question, so maintain context from previous messages. "
                context += "If any requested information is not available, politely inform the user and suggest contacting the seller directly.\n"
                
                # Add specific response templates based on intent
                if intent == 'product_info':
                    if 'price' in analysis['info_needed']:
                        context += "If asked about price, respond with: 'The price is [price] per [unit].'"
                    if 'quantity' in analysis['info_needed']:
                        context += "If asked about quantity, respond with: 'There are [quantity] [unit]s available.'"
                elif intent == 'location':
                    context += "If asked about location, provide the full location details in a clear format."
                elif intent == 'rating':
                    context += "If asked about ratings, mention the average rating and number of ratings if available."
                
                # Combine context and message
                input_text = f"{context}\nUser: {message}\nAssistant:"
                
                # Generate response
                input_ids = self.tokenizer.encode(input_text, return_tensors='pt', padding=True)
                response_ids = self.model.generate(
                    input_ids,
                    max_length=200,
                    pad_token_id=self.tokenizer.pad_token_id,
                    eos_token_id=self.tokenizer.eos_token_id,
                    no_repeat_ngram_size=3,
                    do_sample=True,
                    top_k=50,
                    top_p=0.9,
                    temperature=0.7,
                    num_return_sequences=1
                )
                response = self.tokenizer.decode(response_ids[0], skip_special_tokens=True)
                
                # Extract only the assistant's response
                if "Assistant:" in response:
                    response = response.split("Assistant:")[-1].strip()
                
                # Clean up the response
                response = self._clean_response(response)
                
                # If response is too short or seems incorrect, fall back to rule-based
                if len(response) < 10 or response.startswith("User:") or "Assistant:" in response:
                    response = self._rule_based_response(intent, product_context)
                    
            except Exception as e:
                logger.error(f"Error generating AI response: {str(e)}")
                response = self._rule_based_response(intent, product_context)
            
            # Log the interaction
            self._log_interaction(message, response, intent, 0.8, product_id, session_id)
            
            return response
            
        except Exception as e:
            logger.error(f"Error in generate_response: {str(e)}")
            return "I'm sorry, I encountered an error. Please try again later or contact the seller directly for assistance."

    def _clean_response(self, response: str) -> str:
        """Clean up the response to remove any unwanted content."""
        # Remove any remaining context or prompt markers
        response = response.replace("User:", "").replace("Assistant:", "").strip()
        
        # Remove any template markers
        response = response.replace("[price]", "").replace("[unit]", "").replace("[quantity]", "")
        
        # Remove any empty parentheses
        response = re.sub(r'\(\s*\)', '', response)
        
        # Remove any double spaces
        response = re.sub(r'\s+', ' ', response)
        
        # Remove any leading/trailing punctuation
        response = response.strip('.,!?')
        
        return response

    def _rule_based_response(self, intent: str, product_context: Dict) -> str:
        """Provide rule-based responses when AI model is unavailable."""
        if not product_context:
            return "I'm sorry, I don't have information about this product. Please contact the seller directly for more details."
            
        responses = {
            'greeting': f"Hello! I can help you with information about {product_context.get('name', 'this product')}. What would you like to know?",
            'farewell': "Thank you for your interest! Feel free to ask if you have more questions.",
            'product_info': self._format_product_info_response(product_context),
            'location': self._format_location_response(product_context),
            'contact': self._format_contact_response(product_context),
            'rating': self._format_rating_response(product_context),
            'media': "The product has images and videos available. Would you like to see them?",
            'help': f"I can help you with information about {product_context.get('name', 'this product')}, including pricing, availability, location, and more. What would you like to know?",
            'unknown': self._format_unknown_response(product_context)
        }
        return responses.get(intent, responses['unknown'])

    def _format_unknown_response(self, context: Dict) -> str:
        """Format response for unknown queries."""
        contact_info = context.get('contact', 'N/A')
        if contact_info != 'N/A':
            return f"I'm not sure I understand. For more specific information, you can contact the seller directly at {contact_info}."
        return f"I'm not sure I understand. Could you please rephrase your question about {context.get('name', 'this product')}?"

    def _format_product_info_response(self, context: Dict) -> str:
        """Format product information response."""
        if not context:
            return "I'm sorry, I don't have information about this product. Please contact the seller directly for more details."
        
        response_parts = []
        if context.get('name'):
            response_parts.append(f"The product '{context['name']}'")
        
        if context.get('price') and context.get('unit'):
            response_parts.append(f"costs {context['price']} per {context['unit']}")
        
        if context.get('quantity') and context.get('unit'):
            response_parts.append(f"and there are {context['quantity']} {context['unit']}s available")
        
        if response_parts:
            return " ".join(response_parts) + "."
        return "I'm sorry, I don't have complete information about this product. Please contact the seller directly for more details."

    def _format_location_response(self, context: Dict) -> str:
        """Format location response."""
        if not context or not context.get('location') or context['location'] == 'N/A':
            return "I'm sorry, I don't have location information for this product. Please contact the seller directly for more details."
        return f"The product is available in {context['location']}."

    def _format_contact_response(self, context: Dict) -> str:
        """Format contact information response."""
        if not context or not context.get('contact') or context['contact'] == 'N/A':
            return "I'm sorry, I don't have contact information for this product. Please try checking the seller's profile for contact details."
        return f"You can contact the seller at {context['contact']}."

    def _format_rating_response(self, context: Dict) -> str:
        """Format rating response."""
        if not context or not context.get('rating'):
            return "I'm sorry, I don't have rating information for this product. Please contact the seller directly for more details."
        return f"This product has an average rating of {context['rating']} stars."

    def _log_interaction(self, user_message: str, bot_response: str, intent: str, 
                        confidence: float, product_id: Optional[int] = None, 
                        session_id: Optional[str] = None) -> None:
        """Log the interaction to the database."""
        try:
            ChatLog.objects.create(
                user_message=user_message,
                bot_response=bot_response,
                intent=intent,
                confidence=confidence,
                product_id=product_id,
                session_id=session_id
            )
        except Exception as e:
            logger.error(f"Error logging chat interaction: {str(e)}")

# Create a singleton instance
chatbot = AIChatbot() 