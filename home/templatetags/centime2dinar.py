# Django
from django.utils.translation import get_language
from django import template
from django.utils.html import mark_safe

register = template.Library()

@register.filter(name='centime2dinar')
def centime2dinar(value):
    """ Display centime values to DA """
    new_value = value / 100
    return ("%.2f" % new_value)