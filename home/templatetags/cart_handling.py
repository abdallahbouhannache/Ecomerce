# Django
from django import template

register = template.Library()

@register.filter(name='get_item_message')
def get_item_message(value, arg):
    if value is None: return None
    result = value.get(str(arg), None)
    return result[2] if result else result


@register.filter(name='get_item_quantity')
def get_item_quantity(value, arg):
    if value is None: return None
    result = value.get(str(arg), None)
    return result[1] if result else result


@register.filter(name='get_item_shipping_method')
def get_item_shipping_method(value, arg):
    if value is None: return None
    result = value.get(str(arg), None)
    return result[0] if result else result