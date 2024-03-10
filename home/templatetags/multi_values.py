# Django
from django.utils.translation import get_language
from django import template
from django.utils.html import mark_safe

register = template.Library()

@register.filter(name='multi_name')
def multi_name(value):
    current_language = get_language()
    if current_language == "ar":
        return value.ar_name
    elif current_language == "fr":
        return value.fr_name
    else:
        return value.en_name

@register.filter(name='multi_description')
def multi_description(value):
    current_language = get_language()
    if current_language == "ar":
        return mark_safe(value.ar_description)
    elif current_language == "fr":
        return mark_safe(value.fr_description)
    else:
        return mark_safe(value.en_description)
