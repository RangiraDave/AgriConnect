from typing import Dict, Tuple, Optional, List
import re
import logging
from django.db.models import Avg
from core.models import Product, Profile

logger = logging.getLogger(__name__)

class AIChatbot:
    def __init__(self):
        """Initialize the chatbot (rule-based only, no AI model)."""
        logger.info("Rule-based chatbot initialized.")

    def detect_intent(self, message: str) -> Tuple[str, float]:
        """Detect the intent of the user's message using regex patterns."""
        message = message.lower()
        patterns = {
            # Greetings and farewells
            'greeting': r'\b(hi|hello|hey|greetings|good (morning|afternoon|evening|day|night))\b',
            'farewell': r'\b(bye|goodbye|see you|farewell|see you later|take care)\b',
            # Market information
            'market_price': r'\b(market price|current price|price for|price of|market rate|market value|market trend|trends?|season price|average price|price update)\b',
            'market_trends': r'\b(market trends?|trend for|market analysis|market data|market info|market information|market statistics|market report|market update)\b',
            # Product listing
            'list_product': r'\b(list|add|post|register|upload|submit|create) (my |a |your )?(produce|product|item|goods|harvest|crop|listing)\b',
            'listing_requirements': r'\b(details|information|fields|requirements|what do i need|how to list|how do i list|what should i provide|listing info|listing details)\b',
            'upload_media': r'\b(upload|add|attach|include|post|share) (photo|image|picture|video|media|photos|images|pictures|videos)\b',
            # Communication
            'contact_buyer': r'\b(contact|message|call|reach|talk to|communicate with|negotiate with|connect with) (buyer|customer|interested|person)\b',
            'contact_seller': r'\b(contact|message|call|reach|talk to|communicate with|connect with) (seller|farmer|vendor|cooperative|supplier|owner)\b',
            'negotiate_price': r'\b(negotiate|bargain|discuss|deal|haggle|agree on|set) (price|cost|rate|fee|charge)\b',
            'send_message': r'\b(send|write|leave|drop) (a )?(message|note|inquiry|question|text)\b',
            # Geolocation
            'find_market': r'\b(find|nearest|closest|nearby|local|where is|where can i find|market location|market near|market around|market in) (market|buyer|buyers|place|location|area)\b',
            'see_buyer_location': r'\b(see|view|show|display|locate|find) (buyer|buyers|customer|customers|potential buyer|potential buyers) (location|address|place|area|map)\b',
            'update_location': r'\b(update|change|edit|set|modify) (my |user |profile )?(location|address|place|area|market)\b',
            # User support
            'reset_password': r'\b(reset|forgot|change|recover|lost) (my )?(password|login|credentials)\b',
            'contact_support': r'\b(contact|reach|email|call|support|helpdesk|customer service|admin|administrator|who do i contact|issue|problem|trouble)\b',
            'update_profile': r'\b(update|edit|change|modify|correct) (my |user )?(profile|account|information|details|bio|name|phone|email)\b',
            # Connectivity
            'connectivity_issue': r'\b(no internet|poor internet|connection issue|offline|can\'t access|not loading|not working|slow|network problem|limited internet|unstable connection)\b',
            # Data accuracy
            'report_incorrect_info': r'\b(incorrect|wrong|error|mistake|not correct|not accurate|report|complain|fix|update|change) (price|information|data|listing|details|description|contact|location)\b',
            # User errors
            'edit_listing': r'\b(edit|change|update|correct|fix|modify) (my |a |the )?(listing|product|produce|item|description|price|details|info)\b',
            # Security
            'security': r'\b(security|safe|privacy|protect|protection|secure|data|personal information|suspicious|scam|fraud|report suspicious|report scam|report fraud)\b',
            # Platform limitations
            'platform_down': r'\b(platform|website|site|agriconnect|system) (down|not working|maintenance|unavailable|offline|crash|error|issue|problem)\b',
            # Buying
            'buy_product': r'\b(buy|purchase|order|get|acquire|shop for|looking for|interested in) (product|produce|item|goods|crop|listing)\b',
            'compare_products': r'\b(compare|difference|better|best|quality|price|cheaper|expensive|affordable|value) (products|produce|items|goods|crops|listings)\b',
            # Market analysis
            'market_analysis': r'\b(market analysis|market data|market info|market information|market statistics|market report|market update|market trends?|market insights?)\b',
            # General help
            'help': r'\b(help|assist|guide|how to|what can|tips|advice|query|support|faq|question|how do i|how can i|instructions|manual|usage|use)\b',
            # Fallbacks
            'product_info': r'\b(product|item|details|info|information|describe|explain|about|what is|what are|tell me|more details|learn|know)\b',
            'price': r'\b(price|cost|how much|pricing|fee|charge|rate)\b',
            'quantity': r'\b(quantity|available|in stock|how many|left|remain|stock|units)\b',
            'location': r'\b(where|location|address|place|area|find|near|located|pick up|delivery)\b',
            'contact': r'\b(contact|phone|number|email|reach|call|get in touch|phoning|talking to|seller|vendor|owner|supplier|farmer)\b',
            'rating': r'\b(rating|review|star|feedback|rate|opinion|comment)\b',
            'media': r'\b(picture|image|photo|video|media|see|show)\b',
        }
        for intent, pattern in patterns.items():
            if re.search(pattern, message):
                return intent, 0.9
        if any(word in message for word in ['it', 'this', 'that', 'the', 'one']):
            return 'follow_up', 0.7
        return 'unknown', 0.5

    def get_product_context(self, product_id: Optional[int] = None) -> Dict:
        """Get context about a product if product_id is provided."""
        if not product_id:
            return {}
        try:
            product = Product.objects.select_related(
                'owner__profile__farmer',
                'owner__profile__cooperative'
            ).get(id=product_id)
            location_info = {}
            owner_type = None
            if hasattr(product.owner.profile, 'farmer'):
                location = product.owner.profile.farmer
                owner_type = 'farmer'
                location_info = {
                    'province': location.province.name if location.province else '',
                    'district': location.district.name if location.district else '',
                    'sector': location.sector.name if location.sector else '',
                    'cell': location.cell.name if location.cell else '',
                    'village': location.village.name if location.village else '',
                    'specific_location': location.specific_location or ''
                }
            elif hasattr(product.owner.profile, 'cooperative'):
                location = product.owner.profile.cooperative
                owner_type = 'cooperative'
                location_info = {
                    'province': location.province.name if location.province else '',
                    'district': location.district.name if location.district else '',
                    'sector': location.sector.name if location.sector else '',
                    'cell': location.cell.name if location.cell else '',
                    'village': location.village.name if location.village else '',
                    'specific_location': location.specific_location or ''
                }
            else:
                location_info = None

            def title_label(label, value):
                return f"{label} {value.title()}" if value else ''

            location_str = ""
            if location_info:
                # Build the location string in the requested format
                parts = []
                if location_info['province']:
                    parts.append(f"{location_info['province'].title()} Province")
                if location_info['district']:
                    parts.append(f"{location_info['district'].title()} District")
                if location_info['sector']:
                    parts.append(f"{location_info['sector'].title()} Sector")
                if location_info['cell']:
                    parts.append(f"{location_info['cell'].title()} Cell")
                # Village with 'in' if present
                village_part = ''
                if location_info['village']:
                    village_part = f"in {location_info['village'].title()} Village"
                # Specific location in parentheses if present
                specific = location_info.get('specific_location', '').strip()
                if specific:
                    village_part += f" ({specific})"
                if village_part:
                    parts.append(village_part)
                location_str = ", ".join(parts)
                if not location_str:
                    location_str = "Location not specified"
            else:
                location_str = "Location not available (owner is not a farmer or cooperative)"

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

    def generate_response(self, message: str, product_context: Optional[dict] = None, session_id: Optional[str] = None) -> str:
        """Generate a response based on the user's message (rule-based only)."""
        intent, _ = self.detect_intent(message)
        if not product_context:
            return "I'm sorry, I don't have information about this product. Please contact the seller directly for more details."
        product_name = product_context.get('name', 'this product')

        # Expanded rule-based responses for all intents and edge cases
        if intent == 'greeting':
            return f"Hello! Welcome to AgriConnect. I can help you with information about {product_name} or the platform. What would you like to know?"
        if intent == 'farewell':
            return "Thank you for using AgriConnect! If you have more questions, feel free to ask."
        if intent == 'market_price':
            if product_context.get('price') and product_context.get('unit'):
                return f"The current market price for {product_name} is {product_context['price']} per {product_context['unit']}."
            else:
                return "Sorry, the current market price for this product is not available."
        if intent == 'market_trends' or intent == 'market_analysis':
            return "You can view market trends and analysis on the Market Insights page. We provide up-to-date statistics and trends for all major crops."
        if intent == 'list_product':
            return "To list your produce, go to the 'Add Product' page, fill in the product details, upload photos or videos, and submit. Your product will be visible to buyers after approval."
        if intent == 'listing_requirements':
            return ("When listing a product, you need to provide: name, description, price per unit, available quantity, unit (kg, g, l, unit), contact information, and at least one photo or video. Accurate details help attract buyers!")
        if intent == 'upload_media':
            return "Yes, you can upload photos and videos of your produce when listing a product. This helps buyers see the quality of your goods."
        if intent == 'contact_buyer':
            return "To contact a buyer, use the contact information provided in their profile or respond to their inquiry directly through the platform."
        if intent == 'contact_seller':
            return self._format_contact_response(product_context)
        if intent == 'negotiate_price':
            return "You can negotiate prices directly with buyers or sellers using the provided contact details. Please communicate respectfully and agree on terms before finalizing a deal."
        if intent == 'send_message':
            return "To send a message, use the contact form on the user's profile or the product page. Your message will be delivered to the intended recipient."
        if intent == 'find_market':
            return "You can find the nearest market or buyers using the location filters on the platform. Make sure your profile location is up to date for best results."
        if intent == 'see_buyer_location':
            return "Buyer locations are shown on their profiles and on the product listings. Use the map or address details to find them."
        if intent == 'update_location':
            return "To update your location, go to your profile settings and edit your address. Accurate location helps you connect with nearby buyers and sellers."
        if intent == 'reset_password':
            return "To reset your password, click 'Forgot Password' on the login page and follow the instructions sent to your email."
        if intent == 'contact_support':
            return "If you have issues or need help, contact AgriConnect support at support@agriconnect.com or use the 'Contact Support' form on the website."
        if intent == 'update_profile':
            return "To update your profile information, go to your profile page and click 'Edit Profile'. You can change your name, phone, email, and other details."
        if intent == 'connectivity_issue':
            return ("If you're experiencing connectivity issues, try refreshing the page or checking your internet connection. AgriConnect works best with a stable connection. In areas with limited internet, try accessing the platform during off-peak hours or use the mobile app (if available).")
        if intent == 'report_incorrect_info':
            return ("If you find incorrect information (such as wrong prices or details), please report it using the 'Report' button on the product or contact support. We strive to keep all data accurate.")
        if intent == 'edit_listing':
            return ("To edit your product listing, go to your product page and click 'Edit'. You can update the price, description, and other details. Changes will be reviewed before going live.")
        if intent == 'security':
            return ("Your personal information is protected with industry-standard security measures. If you notice suspicious activity, report it immediately to support@agriconnect.com. Never share your password with anyone.")
        if intent == 'platform_down':
            return ("If the platform is down or under maintenance, please wait and try again later. For urgent issues, contact support. We apologize for any inconvenience.")
        if intent == 'buy_product':
            return ("To buy a product, browse the listings, compare prices and quality, and contact the seller directly using the provided details. You can negotiate and arrange payment and delivery as agreed.")
        if intent == 'compare_products':
            return ("You can compare products by viewing their details, prices, ratings, and media. Use the search and filter options to find the best match for your needs.")
        if intent == 'help':
            return (
                f"I can help you with information about {product_name} and using AgriConnect, including:\n"
                "- Listing or buying products\n"
                "- Market prices and trends\n"
                "- Contacting buyers and sellers\n"
                "- Updating your profile or location\n"
                "- Reporting issues or getting support\n"
                "What would you like to know?"
            )
        if intent == 'product_info':
            return self._format_product_info_response(product_context)
        if intent == 'price':
            if product_context.get('price') and product_context.get('unit'):
                return f"The price of {product_name} is {product_context['price']} per {product_context['unit']}."
            else:
                return "Sorry, price information is not available for this product."
        if intent == 'quantity':
            if product_context.get('quantity') and product_context.get('unit'):
                return f"There are {product_context['quantity']} {product_context['unit']}(s) of {product_name} available."
            else:
                return "Sorry, quantity information is not available for this product."
        if intent == 'location':
            return self._format_location_response(product_context)
        if intent == 'contact':
            return self._format_contact_response(product_context)
        if intent == 'rating':
            return self._format_rating_response(product_context)
        if intent == 'media':
            if product_context.get('media'):
                return "This product has images or videos available. Please check the product page for more."
            else:
                return "No media is available for this product."
        if intent == 'follow_up':
            return f"Could you clarify your question about {product_name}?"
        # Unknown or irrelevant
        return self._varied_unknown_response(product_context)

    def _format_product_info_response(self, context: Dict) -> str:
        """Format product information response."""
        if not context:
            return "I'm sorry, I don't have information about this product. Please contact the seller directly for more details."
        response = f"Product: {context.get('name', 'N/A')}\n"
        if context.get('description'):
            response += f"Description: {context['description']}\n"
        if context.get('price') and context.get('unit'):
            response += f"Price: {context['price']} per {context['unit']}\n"
        if context.get('quantity') and context.get('unit'):
            response += f"Available: {context['quantity']} {context['unit']}(s)\n"
        if context.get('location'):
            response += f"Location: {context['location']}\n"
        if context.get('contact'):
            response += f"Contact: {context['contact']}\n"
        if context.get('rating'):
            response += f"Average rating: {context['rating']}\n"
        return response.strip()

    def _format_location_response(self, context: Dict) -> str:
        """Format location response."""
        location = context.get('location') if context else None
        description = context.get('description') if context else None
        # If structured location is present and not 'Location not specified', use it
        if location and location not in ["N/A", "", "Location not specified", "Location not available (owner is not a farmer or cooperative)"]:
            return f"The product is available in {location}."
        # Fallback: try to extract location from description
        if description:
            # Look for common Rwandan place names or phrases like 'kuva', 'i', 'mu', 'kwa', 'Kigali', etc.
            import re
            match = re.search(r'(kuva [^.,;\n]+|i [^.,;\n]+|mu [^.,;\n]+|kwa [^.,;\n]+|Kigali|Huye|Musanze|Rubavu|Nyagatare|Rwamagana|Kibungo|Gisenyi|Butare|Muhanga|Rusizi|Karongi|Bugesera|Gicumbi|Nyanza|Nyamasheke|Ngoma|Kirehe|Gatsibo|Kamonyi|Rulindo|Gakenke|Burera|Nyabihu|Ngororero|Nyaruguru|Gisagara|Rutsiro|Nyamagabe|Gasabo|Kicukiro|Nyarugenge)', description, re.IGNORECASE)
            if match:
                return f"The product is available in this area: {match.group(0).capitalize()}. (Based on product description)"
            # Otherwise, just use the whole description as a last resort
            return f"Location details are not structured, but the product description says: {description}"
        return "I'm sorry, I don't have location information for this product. Please contact the seller directly for more details."

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

    def _varied_unknown_response(self, context: Dict) -> str:
        """Generate varied unknown responses to avoid repetition."""
        product_name = context.get('name', 'this product')
        fallback_responses = [
            f"I'm not sure I understand. Could you clarify your question about {product_name}?",
            f"Could you rephrase your question about {product_name}? I'd love to help.",
            f"Hmm, I didn't catch that. What would you like to know about {product_name}?",
            f"Sorry, I didn't get that. Please ask about price, availability, location, or contact details for {product_name}.",
        ]
        import random
        return random.choice(fallback_responses)

# Create a singleton instance
chatbot = AIChatbot()