# Django
from django.views import View
from django.utils.translation import gettext_lazy as _
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db import transaction
from django.contrib import messages
# Membership
from membership.forms import RegistrationForm
from membership.models import Member
from membership.decorators import access_not_allowed_for_auth


class Register(View):
    
    @method_decorator(access_not_allowed_for_auth)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    

    def get(self, request):
        form = RegistrationForm()
        context = {
            "form":form,
        }
        return render(request, 'registration/create_account.html', context)

    def post(self, request):
        form = RegistrationForm(request.POST)
        if not form.is_valid():
            context = {
                "form":form,
            }
            return render(request, 'registration/create_account.html', context)
        # If Validation is good, Create a new account
        data = form.cleaned_data
        with transaction.atomic():
            # Create User Instance
            new_user = User.objects.create_user(data['username'], email=data['email'], password=data['password1'])
            if data['first_name']:
                new_user.first_name = data['first_name']
            if data['last_name']:
                new_user.last_name = data['last_name']
            new_user.save()
            # Create Member Instance
            new_member = Member(
                user = new_user,
                phone_number = data['phone_number'],
                address = data['address'] or None,
                wilaya = data['wilaya'] or None,
                commune = data['commune'] or None,
                zip_code = data['zip_code'] or None,
            )
            new_member.save()
            messages.success(request, _("Your account has been created"))
        return redirect('login')