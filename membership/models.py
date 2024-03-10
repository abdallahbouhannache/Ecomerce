# Django
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
# Membership
from membership.abstractions import Shipping

# Create your models here.
class Member(Shipping):
    user     = models.OneToOneField("auth.User", verbose_name=_("User"), on_delete=models.CASCADE)
    merchant = models.BooleanField(_("Merchant"), default=False)
    stores   = models.ManyToManyField("store.Store", verbose_name=_("Store"), blank=True)

    class Meta:
        verbose_name = _("Member")
        verbose_name_plural = _("Members")

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse("member_detail", kwargs={"pk": self.pk})