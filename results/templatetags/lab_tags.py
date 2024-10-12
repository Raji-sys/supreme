from django import template

register = template.Library()

@register.filter(name='split')
def split(value, key):
    """
    Returns the string split by key.
    """
    return value.split(key)
