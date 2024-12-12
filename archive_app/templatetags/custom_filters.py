from django import template

register = template.Library()

@register.filter
def initials(full_name):
    """Returns the initials of the full name."""
    if not full_name:
        return ""
    name_parts = full_name.split()
    if len(name_parts) > 1:
        # First letter of first and last name
        return f"{name_parts[0][0]}{name_parts[-1][0]}".upper()
    return name_parts[0][0].upper()  # Single name fallback
