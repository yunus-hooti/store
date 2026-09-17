from django import template

register = template.Library()

@register.filter
def price_format(value):
    try:
        value = int(value)
    except (ValueError, TypeError):
        return value
    return f"{value:,}"