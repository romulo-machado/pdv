
from django import template

register = template.Library()

@register.filter
def split(value, arg):
    """Divide uma string pelo separador especificado"""
    return value.split(arg)

@register.filter  
def div(value, arg):
    """Divide dois números"""
    try:
        return float(value) / float(arg)
    except (ValueError, ZeroDivisionError):
        return 0
