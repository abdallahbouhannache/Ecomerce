# Django
from django import forms
from django.utils.translation import gettext_lazy as _
# Home
from home.models import Bill, Product
from home.constants import PAYMENT_METHODS
# Captcha
from django_recaptcha.fields import ReCaptchaField


class OrderForm(forms.Form):
    captcha = ReCaptchaField(label = _("Check Captcha"))
    payment_method = forms.ChoiceField(label = _("Payment Options"), choices=PAYMENT_METHODS)

    # # Override Email Field
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['address'].required = True
    #     self.fields['wilaya'].required=True
    #     self.fields['commune'].required=True
    #     self.fields['zip_code'].required=True
    #     # self.fields['zip_code'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        fields = (
            "payment_method",
            "captcha",
        )




class ProductForm(forms.ModelForm):
    
    class Meta:
        model = Product
        exclude = ('store', 'slug', 'deleted', 'purchases', 'rating', 'show')


    def create(self, cleaned_data):
        new_product = Product(**cleaned_data)
        new_product.save()
        return new_product

    def update(self, product):
        product.show = False
        self.save()