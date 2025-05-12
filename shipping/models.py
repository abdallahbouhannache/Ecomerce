# Python
import json
# Django
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from shipping.utils.populate import populate_wilaya_communes, update_database_json


# Create your models here.
class Warehouse(models.Model):
    name = models.CharField(_("Warehouse Name"), max_length=128, unique=True)
    address = models.CharField(_("Address"), max_length=256)

    class Meta:
        verbose_name = _("Warehouse")
        verbose_name_plural = _("Warehouses")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Store old name to detect it when updating
        self.old_name = self.name

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        update_database_json(self)
        super().save(*args, **kwargs)