from django import template

register = template.Library()

@register.filter
def divisor(value, divisor):
    try:
        return value / divisor
    except (ZeroDivisionError, TypeError):
        return 0  # or handle it in a way that makes sense for your application