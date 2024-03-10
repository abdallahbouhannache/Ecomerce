# Django
from django.db import models
from django.utils.translation import ugettext_lazy as _
# Ckeditor
from ckeditor.fields import RichTextField


class Page(models.Model):
    en_title = models.TextField(_("English Title"))
    fr_title = models.TextField(_("French Title"), blank=True, null=True)
    ar_title = models.TextField(_("Arabic Title"), blank=True, null=True)
    en_content = RichTextField(_("English Content"))
    fr_content = RichTextField(_("French Content"), blank=True, null=True)
    ar_content = RichTextField(_("Arabic Content"), blank=True, null=True)


    class Meta:
        abstract = True