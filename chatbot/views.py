from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.shortcuts import get_object_or_404
import re
from core.models import Product

@require_GET
def chatbot_response(request):
    """
    This view handles GET requests for chatbot messages.
    It uses a simple rule-based approach:
      - Initializes the conversation state in the session.
      - Reads a 'message' and 'product_id' parameter from the request.
      - If the state is 'start' or not set, it greets the user and sets state to 'waiting_for_query'.
      - If the state is 'waiting_for_query', it checks the message for keywords like "description", "location",
        or any keyword you want to support.
      - If a keyword is detected and a valid product_id is provided, it queries the Product model and returns relevant details.
      - Otherwise, it asks the user to rephrase.
    Returns:
      A JsonResponse containing the chatbot's response.
    """
    # Initialize session state if not set
    if 'conversation_state' not in request.session:
        request.session['conversation_state'] = 'start'

    state = request.session['conversation_state']
    message = request.GET.get('message', '').lower()
    product_id = request.GET.get('product_id')

    response = ""

    if state == 'start':
        response = "Hello! How can I help you today?"
        request.session['conversation_state'] = 'waiting_for_query'
    elif state == 'waiting_for_query':
        if product_id:
            # Retrieve the product based on the provided product_id
            product = get_object_or_404(Product, id=product_id)
            # Define rule-based responses based on keywords.
            if re.search(r'\b(description|details)\b', message):
                # Return the product description if available; if not, fallback to a default message.
                response = product.description if product.description else "No description available for this product."
            elif re.search(r'\blocation\b', message):
                response = f"This product is available at: {product.location}."
            elif re.search(r'\bprice\b', message):
                response = f"The price per unit is {product.price_per_unit}."
            elif re.search(r'\bquantity\b', message):
                response = f"{product.quantity_available} {product.unit} available."
            elif re.search(r'\bcontacts\b', message):
                response = f"Contact the seller at {product.contact}."
            elif re.search(r'\bimage\b', message):
                response = f"Here is an image of the product: {product.media.url}" if product.media else "No image available for this product."
            elif re.search(r'\bvideo\b', message):
                response = f"Here is a video of the product: {product.media.url}" if product.media else "No video available for this product."
            elif re.search(r'\bthank you\b', message):
                response = "You're welcome! Let me know if you need any more information."
            else:
                response = "Could you please rephrase your question?"
        else:
            response = "Please provide a valid product ID."
    else:
        response = "I'm sorry, I didn't understand that. Could you please rephrase?"

    return JsonResponse({'response': response})
    