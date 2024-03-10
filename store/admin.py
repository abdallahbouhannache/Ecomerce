# Django
from django.contrib import admin
# Store
from store.models import Store

# Register your models here.
@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display  = ["store_name", "wilaya", "commune", "active", "verified"]
    list_filter   = ["store_name", "wilaya", "commune", "active", "verified"]
    search_fields = ["store_name", "first_name", "last_name", "phone_number"]
    readonly_fields = ['slug']
    # fields = [  "first_name",
    #             "last_name",
    #             "phone_number",
    #             "store_name",
    #             'slug',
    #             "logo",
    #             "nif",
    #             "register_commerce",
    #             "address",
    #             "wilaya",
    #             "commune",
    #             "zip_code",
    #             "active",
    #             "verified",
    #         ]
