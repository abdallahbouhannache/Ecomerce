# Django
from django.db import models
from django.utils.translation import gettext_lazy as _
# Membership
from membership.constants import WILAYA_CHOICES, COMMUNE_CHOICES

# Create your models here.
class Shipping(models.Model):
    phone_number = models.CharField(_("Phone Number"), max_length=16)
    address      = models.CharField(_("Address"), max_length=256, blank=True, null=True)
    wilaya       = models.CharField(_("Wilaya"), choices=WILAYA_CHOICES, max_length=64, blank=True, null=True)
    commune      = models.CharField(_("Commune"), choices=COMMUNE_CHOICES, max_length=64, blank=True, null=True)
    zip_code     = models.PositiveIntegerField(_("Zip Code"), blank=True, null=True)
    
    class Meta:
        abstract = True