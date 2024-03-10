# Django
from django.shortcuts import redirect

def only_merchant_allowed(view_func):
    def wrapper_func(request, *args, **kwargs):
        if not request.user.member.merchant:
            return redirect('index')
        return view_func(request, *args, **kwargs)
    return wrapper_func