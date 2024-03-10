# Django
from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe
# Shipping
from shipping.models import Warehouse

# Register your models here.
@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ["name", "address", "show_wilaya"]

    def show_wilaya(self, obj):
        url = reverse('admin_wilaya_list', args=[obj.id])
        template = f"<a target='_blank' class='changelink' href='{url}'>Wilaya Settings</a>"
        return mark_safe(template)
    
    def has_delete_permission(self, request, obj=None):
        return True

