# Python
import uuid
# Django
from django.dispatch import receiver
from django.utils.text import slugify
from django.db.models.signals import post_save
from django.db import models
from django.utils.translation import ugettext_lazy as _
# Membership
from membership.abstractions import Shipping
# Store
from store.uploads import store_logo_path

# Create your models here.
class Store(Shipping):
    owner             = models.ForeignKey("auth.User", verbose_name=_("Store Owner"), on_delete=models.CASCADE)
    first_name        = models.CharField(_("First name"), max_length=64)
    last_name         = models.CharField(_("Last name"), max_length=64)
    store_name        = models.CharField(_("Store Name"), max_length=64, unique=True)
    slug              = models.SlugField(_("Slug"), unique=True, blank=True, null=True)
    logo              = models.ImageField(_("Logo"), upload_to=store_logo_path, blank=True, null=True)
    nif               = models.CharField(_("NIF"), max_length=64)
    register_commerce = models.CharField(_("Register Commerce"), max_length=64)   
    active            = models.BooleanField(_("Active"), default=False, help_text="Approve")
    verified          = models.BooleanField(_("Verified"), default=False, help_text="Give the blue sign")
    bank     = models.CharField(_("Bank Name"), max_length=64, blank=True, null=True)
    rip      = models.CharField(_("Bank RIP"), max_length=64, blank=True, null=True)

    class Meta:
        verbose_name = _("store")
        verbose_name_plural = _("stores")

    def __str__(self):
        if self.store_name:
            return self.store_name
        return f"{self.first_name} {self.last_name}"


# Signals
@receiver(post_save, sender=Store)
def slugify_name(sender, instance, created, **kwargs):
    if created or instance.slug is None:
        text = slugify(instance.store_name)
        extra_text = str(uuid.uuid4())[0:8]
        instance.slug = f"{text}-{extra_text}"
        instance.save()

