# Django
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
# Membership
from membership.constants import WILAYA_CHOICES, COMMUNE_CHOICES

class MemberForm(forms.ModelForm):
    # new Fields
    phone_number = forms.CharField(label=_('Phone Number'), required=True, help_text=_('For example: 0770605062 or +213770209494'))
    address = forms.CharField(label=_('Address'), required=True, help_text=_('For example: 123 Cité Les Arbres'))
    wilaya = forms.ChoiceField(label=_('Wilaya'), required=True, help_text=_('Wilaya example: Constantine'), choices=WILAYA_CHOICES)
    commune = forms.ChoiceField(label=_('Commune'), required=True, help_text=_('Commune example: Béni Hamidane'), choices=COMMUNE_CHOICES)
    zip_code = forms.CharField(
        label=_('Zip Code'),
        required=True,
        help_text=_('Zip Code example: 25220'),
        widget=forms.TextInput(attrs={'type':'number', 'min':0})
    )


    def clean_email(self):
        email = self.data.get('email')
        # Check if user exist
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        else:
            raise forms.ValidationError(
                    _("Email is already taken by another user."))



class RegistrationForm(UserCreationForm, MemberForm):

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")



class UpdateForm(MemberForm):

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", )
        exclude = ('username', 'email', 'phone_number')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('phone_number')