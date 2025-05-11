from django import template
from django.utils import timezone

register = template.Library()

@register.filter
def concise_timesince(value):
    """
    Returns a concise, user-friendly 'time since' string.
    """
    if not value:
        return ""
    now = timezone.now()
    diff = now - value

    seconds = int(diff.total_seconds())
    minutes = seconds // 60
    hours = minutes // 60
    days = diff.days
    months = days // 30
    years = days // 365

    if seconds < 60:
        return "just now"
    elif minutes < 60:
        return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
    elif hours < 24:
        return f"{hours} hour{'s' if hours != 1 else ''} ago"
    elif days < 30:
        return f"{days} day{'s' if days != 1 else ''} ago"
    elif months < 12:
        return f"{months} month{'s' if months != 1 else ''} ago"
    else:
        return f"{years} year{'s' if years != 1 else ''} ago"
