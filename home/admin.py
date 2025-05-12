# Django
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
# Home
from home.models import Category, Product, Order, Subscriber, Bill, Carousel


# Administration Title
admin.site.site_header = _("Elamane Communication and Contact")


@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ["user", "key", "orderID", "payment_option", "total", 'is_paid']
    readonly_fields = ['create_date', 'auto_delete_at']
    list_filter = ["payment_option", 'is_paid', 'status']

    def total(self, obj):
        if obj.products_price is None or obj.shipping_price is None: return None
        return f"{obj.products_price + obj.shipping_price} DA"
    
    total.short_description = _("Bill Total")

@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ["email", "unsubscribe_code", ]
    search_fields = ['email']
    readonly_fields = ['unsubscribe_code']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["en_name", "fr_name", "ar_name", "icon", ]
    readonly_fields = ['slug']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["en_name", "stock", "fr_name", "ar_name", "price", "commission_"]
    search_fields = ["en_name", "ar_name" , "fr_name"]
    list_filter = ["category"]
    readonly_fields = ['slug']

    def price(self, obj):
        return f"{obj.current_price} DA"
    
    def commission_(self, obj):
        return f"{obj.commission} DA"

    price.short_description = _("Price")
    commission_.short_description = _("Commission")



@admin.register(Carousel)
class CarouselAdmin(admin.ModelAdmin):
    list_display = ["name", "order"]



@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass