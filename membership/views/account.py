# Django
from django.views import View
from django.utils.translation import ugettext_lazy as _
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import transaction
# Membership
from membership.forms import UpdateForm
from membership.models import Member


class Account(View):
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    

    def init_data(self, request):
        data = {
            'username':request.user.username,
            'first_name':request.user.first_name,
            'last_name':request.user.last_name,
            'email':request.user.email,
            'phone_number':request.user.member.phone_number,
            'address':request.user.member.address,
            'wilaya':request.user.member.wilaya,
            'commune':request.user.member.commune,
            'zip_code':str(request.user.member.zip_code),
        }
        return data


    def get(self, request):
        data = self.init_data(request)
        form = UpdateForm(initial=data)
        context = {
            "form":form,
        }
        return render(request, 'membership/edit_account.html', context)

    def post(self, request):
        data = self.init_data(request)
        form = UpdateForm(request.POST, initial=data)
        if form.has_changed():
            if form.is_valid():
                for field in form.changed_data:
                    try:
                        target_field = getattr(request.user, field)
                        setattr(request.user, field, form.cleaned_data[field])
                        request.user.save()
                    except:
                        target_field = getattr(request.user.member, field)
                        setattr(request.user.member, field, form.cleaned_data[field])
                        request.user.member.save()
                messages.success(request, _("Your account informations has been updated"))
                next_ = request.POST.get("next", 'index')
                return redirect(next_)
            else:
                context = {
                    "form":form,
                }
                return render(request, 'membership/edit_account.html', context)
        return redirect('account_display')
