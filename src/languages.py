# Django
from django.utils import translation
from django.shortcuts import redirect
from django.conf import settings

def i18n_switcher(request, prefix):
    try:
        allowed_languages = ['ar', 'fr', 'en']
        if prefix in allowed_languages:
            translation.activate(prefix)
            response = redirect(request.META.get('HTTP_REFERER'))
            response.set_cookie(settings.LANGUAGE_COOKIE_NAME, prefix)
    except:
        pass
    return response