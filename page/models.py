# Django
from django.db import models
from django.utils.translation import ugettext_lazy as _
# Page
from page.abstractions import Page


# Create your models here.
class PrivacyPolicy(Page):
    
    class Meta:
        verbose_name = _("Privacy Policy")
        verbose_name_plural = _("Privacy Policy")

    def __str__(self):
        return self.en_content


class TermOfUse(Page):
    
    class Meta:
        verbose_name = _("Term Of Use")
        verbose_name_plural = _("Term Of Use")

    def __str__(self):
        return self.en_content


class TrackMyOrder(Page):
    
    class Meta:
        verbose_name = _("Track Orders")
        verbose_name_plural = _("Track Orders")

    def __str__(self):
        return self.en_content


class CancelOrders(Page):
    
    class Meta:
        verbose_name = _("Cancel Orders")
        verbose_name_plural = _("Cancel Orders")

    def __str__(self):
        return self.en_content


class ReturnRefund(Page):
    
    class Meta:
        verbose_name = _("Return & Refund")
        verbose_name_plural = _("Return & Refund")

    def __str__(self):
        return self.en_content


class AboutUs(Page):
    
    class Meta:
        verbose_name = _("About Us")
        verbose_name_plural = _("About Us")

    def __str__(self):
        return self.en_content


class ContactUs(Page):
    
    class Meta:
        verbose_name = _("Contact Us")
        verbose_name_plural = _("Contact Us")

    def __str__(self):
        return self.en_content



ACTIVE_MODELS = {
    "privacy-policy":PrivacyPolicy,
    "term-of-use":TermOfUse,
    "track-my-order":TrackMyOrder,
    "cancel-orders":CancelOrders,
    "return-refund":ReturnRefund,
    "about-us":AboutUs,
    "contact-us":ContactUs,
}

def page_caller(slug):
    return ACTIVE_MODELS.get(slug, None)