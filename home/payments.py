# Python
import requests, urllib
# Django
from django.conf import settings
from django.db import transaction
from django.utils.translation import get_language
from django.utils.translation import ugettext_lazy as _
# Home
from home.models import Bill


def satim_params_generator(key, amount, description):
    returnUrl = f'{settings.HTTP_PROTOCOL}://{settings.HTTP_HOST}/success/'
    failUrl = f'{settings.HTTP_PROTOCOL}://{settings.HTTP_HOST}/fail/'
    form = {
        'userName':settings.SATIM_USERNAME,
        'password':settings.SATIM_PASSWORD,
        'orderNumber':key,
        'amount':amount,
        'currency':'012', # Algerian Dinar code according to ISO4217
        'description':description,
        'language':get_language(),
    }
    pre_params = f'{urllib.parse.urlencode(form)}&returnUrl={returnUrl}&failUrl={failUrl}'
    params = pre_params + f'&jsonParams={{"force_terminal_id":"{settings.SATIM_ID}","udf1":"example"}}'
    return params


def initilize_create_satim_bill(key, amount, description=""):
    """ Create a payment url in STAIM """
    url = settings.SATIM_CREATE_API
    params = satim_params_generator(key, amount, description)
    request = requests.get(f'{url}{params}')
    response = request.json()
    return request.status_code, response # Always check errorCode, if exist then it will apear in errorMessage


def create_satim_bill(user, key, form_data, satim_response_data, products_price, shipping_price, orders):
    """ Create a Bill in this platform after validated check from SATIM """
    # Initilize Bill
    with transaction.atomic():
        new_bill = Bill(
            first_name     = form_data['first_name'],
            last_name      = form_data['last_name'],
            phone_number   = form_data['phone_number'],
            key            = key,
            address        = form_data['address'],
            wilaya         = form_data['wilaya'],
            commune        = form_data['commune'],
            zip_code       = form_data['zip_code'],
            user           = user,
            products_price = products_price,
            shipping_price = shipping_price,
            payment_option = "direct",
            status         = "Waiting",
            orderID        = satim_response_data.get('orderId', None),
            payURL         = satim_response_data.get('formUrl', None),
        )
        new_bill.save()
        if orders:
            new_bill.orders.add(*orders)
            new_bill.save()
        return new_bill


def initilize_check_satim_bill(orderID):
    """ Check an order in STAIM """
    if not orderID:
        return 404, {
            "ErrorCode": 404,
            "ErrorMessage": _("Order ID is required"),
            "actionCodeDescription": _("You are not allowed to access here."),
            }
    url = settings.SATIM_CONFIRM_API
    form = {
        'userName':settings.SATIM_USERNAME,
        'password':settings.SATIM_PASSWORD,
        'orderId':orderID,
        'language':get_language(),
    }
    request = requests.get(url, params=form)

    response = request.json()
    return request.status_code, response
