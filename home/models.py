# Python
import uuid
import datetime
# Django
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.utils.text import slugify
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import get_language
# Ckeditor
from ckeditor.fields import RichTextField
# Home
from home.abstractions import Naming
from home.uploads import thumbs_path, product_images_path
from home.constants import PAYMENT_METHODS
# Membership
from membership.abstractions import Shipping


def set_expire():
    """ Expire Bill if not paid after certin amount """
    return timezone.now() + datetime.timedelta(hours=24)


def store_carousel_path(instance, filename):
    return f'carousel/{filename}'


# Create your models here.
class Category(Naming):
    """
    We can create each category with it's logo, By FontAwesome.
    """
    icon = models.CharField(_("Icon Code"), max_length=64)
    
    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        current_language = get_language()
        return self.ar_name if current_language == "ar" else self.fr_name if current_language == "fr" else self.en_name




class Product(Naming):
    """
    The Product Model
    """
    show           = models.BooleanField(_("Show"), default=False, help_text=_("Hide/Display this product"))
    deleted        = models.BooleanField(_("Deleted"), default=False, help_text=_("Merchant mark this item as deleted"))
    category       = models.ForeignKey("home.Category", verbose_name=_("Category"), on_delete=models.CASCADE, help_text=_("Please choose a category"))
    store          = models.ForeignKey("store.Store", verbose_name=_("Store"), on_delete=models.CASCADE, blank=True, null=True, help_text=_("Store who selling this product"))
    warehouse      = models.ForeignKey("shipping.Warehouse", verbose_name=_("Warehouse"), on_delete=models.CASCADE, help_text=_("Warehouse where this product is stored"))
    ar_description = RichTextField(_("Arabic Description"), blank=True, null=True, help_text=_("Write a description in Arabic"))
    fr_description = RichTextField(_("French Description"), blank=True, null=True, help_text=_("Write a description in French"))
    en_description = RichTextField(_("English Description"), blank=True, null=True, help_text=_("Write a description in English"))
    thumbnail      = models.ImageField(_("Thumbnail"), upload_to=thumbs_path, help_text=_("Add a thumbnail for this product"))
    image1         = models.ImageField(_("Image 1"), upload_to=product_images_path, blank=True, null=True)
    image2         = models.ImageField(_("Image 2"), upload_to=product_images_path, blank=True, null=True)
    image3         = models.ImageField(_("Image 3"), upload_to=product_images_path, blank=True, null=True)
    image4         = models.ImageField(_("Image 4"), upload_to=product_images_path, blank=True, null=True)
    stock          = models.PositiveIntegerField(_("Stock"), default=1, help_text=_("How many items you have to stock?"))
    prev_price     = models.DecimalField(_("Previous Price"), max_digits=15, decimal_places=2, blank=True, null=True, help_text=_("The previouse price of this product"))
    current_price  = models.DecimalField(_("Current Price"), max_digits=15, decimal_places=2, help_text=_("The current price of this product"))
    commission     = models.DecimalField(_("Commission"), max_digits=15, decimal_places=2, default=0, help_text=_("How much do you want our commission for each product sold?"))
    purchases      = models.PositiveIntegerField(_("Number Of Purchases"), default=0)
    rating         = models.PositiveIntegerField(_("Rating"), default=0, help_text=_("Rating from 0 to 5"))
    length         = models.DecimalField(_("Length (m)"), max_digits=5, decimal_places=2, help_text=_("Length of this product in meter"))
    width          = models.DecimalField(_("Width (m)"), max_digits=5, decimal_places=2, help_text=_("Width of this product in meter"))
    height         = models.DecimalField(_("Height (m)"), max_digits=5, decimal_places=2, help_text=_("Height of this product in meter"))
    weight         = models.DecimalField(_("Weight (Kg)"), max_digits=5, decimal_places=2, help_text=_("Weight of this product in kilogram"))
    created_date   = models.DateTimeField(_("Created at"), auto_now=False, auto_now_add=True)

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    
    def get_name(self):
        current_language = get_language()
        return self.ar_name if current_language == "ar" else self.fr_name if current_language == "fr" else self.en_name

    def sell_price(self):
        """
        The client should see the total price with our commission
        """
        return self.current_price + self.commission

    def free_shipping(self):
        return 0.0

    def __str__(self):
        current_language = get_language()
        return self.ar_name if current_language == "ar" else self.fr_name if current_language == "fr" else self.en_name



class Order(models.Model):
    """
    Every Bill have multiple orders, we handling each order independentally
    and collect them in one bill.
    """
    order_date       = models.DateTimeField(_("Order Date"), auto_now=False, auto_now_add=True)
    product          = models.ForeignKey("home.Product", verbose_name=_("Product"), on_delete=models.CASCADE)
    quantity         = models.PositiveIntegerField(_("Quantity"), default=1)
    individual_price = models.DecimalField(_("Individual Price"), max_digits=15, decimal_places=2)
    message          = models.TextField(_("Message"), blank=True, null=True)
    ship_date        = models.DateTimeField(_("Ship Date"), blank=True, null=True)

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")

    def current_price(self):
        """
        The price can be changed later, the order price will be saved fixed
        but if we want to compare the price when the user buy this item with the current price
        we can call this method
        """
        price = self.product.current_price * self.quantity
        return price

    def __str__(self):
        current_language = get_language()
        return self.product.ar_name if current_language == "ar" else self.product.fr_name if current_language == "fr" else self.product.en_name



class Bill(Shipping):
    """
    User can create Bills, and the Bill is a group of multiple Bills
    shipping_price will calculated when form submitted.
    """
    STATUS = [
        ("Waiting", _("Waiting")),
        ("Shipped", _("Shipped")),
        ("Completed", _("Completed")),
        ("Returned", _("Returned")),
        ("Canceled", _("Canceled")),
        ("Refunded", _("Refunded")),
    ]
    first_name     = models.CharField(_("First Name"), max_length=256, help_text=_('First Name at Elamamecc'))
    last_name      = models.CharField(_("Last Name"), max_length=256, help_text=_('Last Name at Elamamecc'))
    key            = models.PositiveIntegerField(_("Key"), blank=True, null=True, help_text=_('Order ID of Elamanecc'))
    user           = models.ForeignKey("auth.User", verbose_name=_("User"), on_delete=models.CASCADE)
    orders         = models.ManyToManyField("home.Order", verbose_name=_("Orders"), blank=True)
    products_price = models.DecimalField(_("Products Price"), max_digits=15, decimal_places=2, blank=True, null=True)
    shipping_price = models.DecimalField(_("Shipping Price"), max_digits=15, decimal_places=2, blank=True, null=True)
    payment_option = models.CharField(_("Payment Option"), choices=PAYMENT_METHODS,max_length=50)
    orderID        = models.CharField(_("Order ID"), max_length=64, blank=True, null=True, help_text=_('Order Number of SATIM'))
    order_status   = models.IntegerField(_("Order Status"), help_text=_('Order Status of SATIM'), blank=True, null=True)
    error_code     = models.IntegerField(_("Error Code"), help_text=_('Error Code of SATIM'), blank=True, null=True)
    error_message  = models.TextField(_("Error Message"), help_text=_('Error Message of SATIM'), blank=True, null=True)
    action_code    = models.IntegerField(_("Action Code"), help_text=_('Action Code of SATIM'), blank=True, null=True)
    action_code_description = models.TextField(_("Action Code Description"), help_text=_('Action Code Description of SATIM'), blank=True, null=True)
    SVFE_response  = models.CharField(_("SVFE Response"), max_length=63, help_text=_('SVFE Response of the SATIM card'), blank=True, null=True)
    pan            = models.CharField(_("PAN"), max_length=63, help_text=_('Masked number of the SATIM card'), blank=True, null=True)
    expiration     = models.CharField(_("Expiration"), max_length=63, help_text=_('Expiration date of the SATIM card'), blank=True, null=True)
    cardholder_name = models.TextField(_('Cardholder Name'), help_text=_('Cardholder Name of SATIM client'), blank=True, null=True)
    amount         = models.PositiveIntegerField(_("Amount"), help_text=_('Amount should paid in centime with SATIM'), blank=True, null=True)
    deposit_amount = models.PositiveIntegerField(_("Deposit Amount"), help_text=_('Paid Amount in centime with SATIM'), blank=True, null=True)
    currency_code  = models.CharField(_("Currency Code"), max_length=32, help_text=_('Currency Code ISO4217'), blank=True, null=True)
    approval_code  = models.CharField(_("Approval Code"), max_length=6, help_text=_('Approval Code of SATIM'), blank=True, null=True)
    auth_code      = models.IntegerField(_("Auth Code"), help_text=_('Auth Code of SATIM should always be 2'), blank=True, null=True)
    ip             = models.CharField(_("IP"), help_text=_('Address IP of SATIM client'), max_length=32, blank=True, null=True)
    payURL         = models.TextField(_("Payment URL"), blank=True, null=True)
    client_id      = models.CharField(_("Client ID"), max_length=63, help_text=_('Client ID of SATIM'), blank=True, null=True)
    binding_id     = models.CharField(_("Client ID"), max_length=63, help_text=_('Binding ID of SATIM'), blank=True, null=True)
    is_paid        = models.BooleanField(_("Is Paid ?"), default=False)
    create_date    = models.DateTimeField(_("Create Date"), auto_now=False, auto_now_add=True)
    auto_delete_at = models.DateTimeField(_("Auto Delete Date"), default=set_expire, help_text=_('Time after deleting this bill of not paid')) 
    status         = models.CharField(_("Status"), choices=STATUS, max_length=32, help_text=_('Status of Elamanecc'))
    params         = models.TextField(_('Params'), help_text=_('Params of SATIM client'), blank=True, null=True)

    class Meta:
        verbose_name = _("Bill")
        verbose_name_plural = _("Bills")

    def bill_total(self):
        if self.products_price is None or self.shipping_price is None:
            return None
        return round(self.products_price + self.shipping_price, 2)

    def __str__(self):
        return self.user.username




class Subscriber(models.Model):
    email = models.EmailField(_("Email"), max_length=254)
    unsubscribe_code = models.UUIDField(_("Unsubscribe Code"), default=uuid.uuid4)

    class Meta:
        verbose_name = _("Subscriber")
        verbose_name_plural = _("Subscribers")

    def __str__(self):
        return self.email




class Carousel(models.Model):
    name  = models.CharField(_("Name"), max_length=32)
    image = models.ImageField(_("Image"), upload_to=store_carousel_path)
    order = models.PositiveIntegerField(_("Order"))
    is_hide = models.BooleanField(_("Hide"), default=False)

    class Meta:
        verbose_name = _("Carousel")
        verbose_name_plural = _("Carousel")

    def __str__(self):
        return self.name




# Signals
@receiver(post_save, sender=Category)
@receiver(post_save, sender=Product)
def slugify_name(sender, instance, created, **kwargs):
    if created or instance.slug is None:
        text = slugify(instance.en_name)
        extra_text = str(uuid.uuid4())[0:8]
        instance.slug = f"{text}-{extra_text}"
        instance.save()

