# Django
from django.utils import timezone
from django import template

register = template.Library()

def check_delete_deadline(value):
    if timezone.now() > value : return False
    return True

@register.filter(name='allow_delete')
def allow_delete(value):
    """ Allow User to cancel a bill """
    return check_delete_deadline(value)