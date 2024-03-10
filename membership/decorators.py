# Django
from django.shortcuts import redirect

def access_not_allowed_for_auth(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')
        return view_func(request, *args, **kwargs)
    return wrapper_func