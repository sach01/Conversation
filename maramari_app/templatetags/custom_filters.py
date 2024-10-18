# maramari_app/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def has_role(user, role_name):
    """Check if the user has a specific role."""
    return user.has_role(role_name)  # Assuming the method has_role exists on your user model
