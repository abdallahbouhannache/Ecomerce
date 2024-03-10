# Django
from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
# Home
from home.models import Subscriber


class Subscribe(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request):
        email = request.POST.get('email')
        next_ = request.POST.get('next')
        try:
            cleaned_email = validate_email(email)
        except Exception as e:
            template = _("Please fix these errors:")
            for error in e:
                template += f" {error}"
            messages.error(request, template)
        else:
            obj, created = Subscriber.objects.get_or_create(
                email=email,
            )
            if created:
                # TODO: Send welcome message
                pass
                messages.success(request, _(f"{email} has been subscribed to our newsletter"))
            else:
                messages.warning(request, _(f"{email} already subscribed to our newsletter"))
        return redirect(next_)