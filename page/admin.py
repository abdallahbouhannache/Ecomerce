# Django
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
# Page
from page.models import (
    PrivacyPolicy,
    TermOfUse,
    TrackMyOrder,
    CancelOrders,
    ReturnRefund,
    AboutUs,
    ContactUs,
)

# Register your models here.


@admin.register(PrivacyPolicy)
class PrivacyPolicyAdmin(admin.ModelAdmin):
    list_display = ["display_label"]

    def has_add_permission(self, request, obj=None):
        # Allow only one entry PrivacyPolicy
        count = PrivacyPolicy.objects.all().count()
        if count >= 1:
            return False
        return True

    def display_label(self, obj):
        return _("Privacy Policy")


@admin.register(TermOfUse)
class TermOfUseAdmin(admin.ModelAdmin):
    list_display = ["display_label"]

    def has_add_permission(self, request, obj=None):
        # Allow only one entry TermOfUse
        count = TermOfUse.objects.all().count()
        if count >= 1:
            return False
        return True

    def display_label(self, obj):
        return _("Term Of Use")


@admin.register(TrackMyOrder)
class TrackMyOrderAdmin(admin.ModelAdmin):
    list_display = ["display_label"]

    def has_add_permission(self, request, obj=None):
        # Allow only one entry TrackMyOrder
        count = TrackMyOrder.objects.all().count()
        if count >= 1:
            return False
        return True

    def display_label(self, obj):
        return _("Track My Order")

@admin.register(CancelOrders)
class CancelOrdersAdmin(admin.ModelAdmin):
    list_display = ["display_label"]

    def has_add_permission(self, request, obj=None):
        # Allow only one entry CancelOrders
        count = CancelOrders.objects.all().count()
        if count >= 1:
            return False
        return True

    def display_label(self, obj):
        return _("Cancel Orders")


@admin.register(ReturnRefund)
class ReturnRefundAdmin(admin.ModelAdmin):
    list_display = ["display_label"]

    def has_add_permission(self, request, obj=None):
        # Allow only one entry ReturnRefund
        count = ReturnRefund.objects.all().count()
        if count >= 1:
            return False
        return True

    def display_label(self, obj):
        return _("Return & Refund")


@admin.register(AboutUs)
class AboutUsAdmin(admin.ModelAdmin):
    list_display = ["display_label"]

    def has_add_permission(self, request, obj=None):
        # Allow only one entry AboutUs
        count = AboutUs.objects.all().count()
        if count >= 1:
            return False
        return True

    def display_label(self, obj):
        return _("About Us")


@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ["display_label"]

    def has_add_permission(self, request, obj=None):
        # Allow only one entry ContactUs
        count = ContactUs.objects.all().count()
        if count >= 1:
            return False
        return True

    def display_label(self, obj):
        return _("Contact Us")