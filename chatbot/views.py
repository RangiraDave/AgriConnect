# chatbot/views.py
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
import re
from core.models import Product, Profile
from django.db.models import Avg
import logging

logger = logging.getLogger(__name__)

@require_GET
def chatbot_response(request):
    """
    Enhanced chatbot for AgriConnect that provides intelligent responses about products,
    market insights, and general agricultural information.
    """
    try:
        # Initialize session variables if they don't exist
        if not request.session.get('conversation_state'):
            request.session['conversation_state'] = 'start'
        if not request.session.get('context'):
            request.session['context'] = {}

        state = request.session['conversation_state']
        context = request.session['context']
        message = request.GET.get('message', '').lower()
        product_id = request.GET.get('product_id')
        user_name = request.user.username if request.user.is_authenticated else "Guest"

        response = ""
        
        # Common greetings and farewells
        greetings = [' hello ', ' hi ', ' hey ', ' greetings ', ' good morning ', ' good afternoon ', ' good evening ']
        farewells = ['bye', 'goodbye', 'see you', 'thank you', 'thanks']
        
        # Check for greetings
        if any(greeting in message for greeting in greetings):
            if product_id:
                try:
                    product = get_object_or_404(Product, id=product_id)
                    response = _("Hello {user_name}! I'm AgriConnect Assistant. I can help you with information about {product_name}. What would you like to know?").format(
                        user_name=user_name,
                        product_name=product.name
                    )
                except Product.DoesNotExist:
                    response = _("I'm sorry, I couldn't find that product. How else can I help you?")
            else:
                response = _("Hello {user_name}! I'm AgriConnect Assistant. How can I help you today?").format(
                    user_name=user_name
                )
            request.session['conversation_state'] = 'waiting_for_query'
            return JsonResponse({'response': response})

        # Check for farewells
        if any(farewell in message for farewell in farewells):
            response = _("Thank you for using AgriConnect! If you have any more questions, feel free to ask. Have a great day!")
            request.session['conversation_state'] = 'start'
            request.session['context'] = {}  # Reset context on farewell
            return JsonResponse({'response': response})

        if state == 'start':
            if product_id:
                try:
                    product = get_object_or_404(Product, id=product_id)
                    response = _("Hello {user_name}, I'm AgriConnect Assistant. I can help you with information about {product_name}. What would you like to know?").format(
                        user_name=user_name,
                        product_name=product.name
                    )
                except Product.DoesNotExist:
                    response = _("I'm sorry, I couldn't find that product. How else can I help you?")
            else:
                response = _("Hello! I'm AgriConnect Assistant. How can I help you today?")
            request.session['conversation_state'] = 'waiting_for_query'
        
        elif state == 'waiting_for_query':
            if product_id:
                try:
                    product = get_object_or_404(Product, id=product_id)
                    owner = product.owner
                    owner_profile = Profile.objects.get(user=owner)
                    
                    # Calculate average rating
                    avg_rating = product.ratings.aggregate(Avg('rating'))['rating__avg'] or 0
                    rating_count = product.ratings.count()
                    
                    # Define comprehensive response patterns
                    if re.search(r'\b(description|details|about)\b', message):
                        response = product.description if product.description else _("No detailed description available for this product.")
                    
                    elif re.search(r'\b(location|where|place)\b', message):
                        location_info = []
                        if owner_profile.role == 'umuhinzi':
                            farmer = owner_profile.farmer
                            if farmer:
                                location_info = [
                                    farmer.province.name if farmer.province else None,
                                    farmer.district.name if farmer.district else None,
                                    farmer.sector.name if farmer.sector else None,
                                    farmer.cell.name if farmer.cell else None,
                                    farmer.village.name if farmer.village else None,
                                    farmer.specific_location
                                ]
                        elif owner_profile.role == 'cooperative':
                            cooperative = owner_profile.cooperative
                            if cooperative:
                                location_info = [
                                    cooperative.province.name if cooperative.province else None,
                                    cooperative.district.name if cooperative.district else None,
                                    cooperative.sector.name if cooperative.sector else None,
                                    cooperative.cell.name if cooperative.cell else None,
                                    cooperative.village.name if cooperative.village else None,
                                    cooperative.specific_location
                                ]
                        
                        location_info = [loc for loc in location_info if loc]
                        response = _("This product is available in: {location}").format(
                            location=", ".join(location_info) if location_info else _("Location information not available")
                        )
                    
                    elif re.search(r'\b(price|cost|how much)\b', message):
                        response = _("The price is {price} per {unit} of {product_name}.").format(
                            price=product.price_per_unit,
                            unit=product.unit,
                            product_name=product.name
                        )
                    
                    elif re.search(r'\b(quantity|available|stock)\b', message):
                        response = _("There are {quantity} {unit} of {product_name} available.").format(
                            quantity=product.quantity_available,
                            unit=product.unit,
                            product_name=product.name
                        )
                    
                    elif re.search(r'\b(contact|phone|number|reach|"seller\'s contact"|"seller\'s phone"|"seller\'s number")\b', message):
                        response = _("You can contact the seller at {phone}. The seller is a {role}.").format(
                            phone=owner_profile.phone or _("Contact information not available"),
                            role=owner_profile.role
                        )
                    
                    elif re.search(r'\b(rating|review|feedback)\b', message):
                        if rating_count > 0:
                            response = _("This product has an average rating of {rating:.1f} stars from {count} reviews.").format(
                                rating=avg_rating,
                                count=rating_count
                            )
                        else:
                            response = _("This product hasn't received any ratings yet.")
                    
                    elif re.search(r'\b(image|photo|picture|"show me")\b', message):
                        if product.media and not product.is_video():
                            response = _("Here is an image of the product: {url}").format(url=product.media.url)
                        else:
                            response = _("No image is available for this product.")
                    
                    elif re.search(r'\b(video|watch|"show me video")\b', message):
                        if product.media and product.is_video():
                            response = _("Here is a video of the product: {url}").format(url=product.media.url)
                        else:
                            response = _("No video is available for this product.")
                    
                    elif re.search(r'\b(seller|owner|producer|"seller\'s name"|who)\b', message):
                        response = _("This product is sold by {username}, who is a {role}. You can contact them at {phone}.").format(
                            username=owner.username,
                            role=owner_profile.role,
                            phone=owner_profile.phone
                        )
                    
                    elif re.search(r'\b(help|assist|support)\b', message):
                        response = _("I can help you with information about:\n"
                                   "- Product details and description\n"
                                   "- Price and availability\n"
                                   "- Location and contact information\n"
                                   "- Ratings and reviews\n"
                                   "- Images and videos\n"
                                   "- Seller information\n"
                                   "What would you like to know?")

                    else:
                        response = _("Please clarify your question. I can help you with information about this product's:\n"
                                   "- Description\n"
                                   "- Price\n"
                                   "- Quantity\n"
                                   "- Location\n"
                                   "- Contact details\n"
                                   "- Ratings\n"
                                   "- Media (images/videos)\n"
                                   "What would you like to know?")
                except (Product.DoesNotExist, Profile.DoesNotExist) as e:
                    logger.error(f"Error accessing product or profile: {str(e)}")
                    response = _("I'm sorry, I encountered an error while retrieving the product information. Please try again later.")
            else:
                response = _("I can help you browse products, provide market insights, or answer questions about AgriConnect. What would you like to know?")

        return JsonResponse({'response': response})
    
    except Exception as e:
        logger.error(f"Error in chatbot_response: {str(e)}")
        return JsonResponse({
            'response': _("I'm sorry, I encountered an error. Please try again later.")
        }, status=500)
