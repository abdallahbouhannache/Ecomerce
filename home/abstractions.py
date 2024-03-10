# Python
import uuid
# Django
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.dispatch import receiver

# Create your models here.
class Naming(models.Model):
    ar_name = models.CharField(_("Arabic Name"), max_length=256, help_text=_("Write name in Arabic"))
    fr_name = models.CharField(_("French Name"), max_length=256, help_text=_("Write name in French"))
    en_name = models.CharField(_("English Name"), max_length=256, help_text=_("Write name in English"))
    slug    = models.SlugField(_("Slug"), unique=True, blank=True, null=True)
    
    class Meta:
        abstract = True


