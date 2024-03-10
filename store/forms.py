# Django
from django import forms
# Store
from store.models import Store


class StoreForm(forms.ModelForm):

    class Meta:
        model = Store
        fields = (
            "store_name",
            "nif",
            "register_commerce",
            "logo",
            "first_name",
            "last_name",
            "phone_number",
            "wilaya",
            "commune",
            "zip_code",
            "bank",
            "rip",
        )
