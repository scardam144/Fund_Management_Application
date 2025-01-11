# admin_panel/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0  # Return 0 if there's an error with the multiplication

@register.filter
def subtract(value, arg):
    """Subtract arg from value, safely handling strings."""
    try:
        value = float(value)
        arg = float(arg)
    except (ValueError, TypeError):
        return 0  # Return 0 if conversion fails
    return value - arg