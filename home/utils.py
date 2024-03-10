# Python
from random import randint
import json
# Django
from django.conf import settings
from django.db import transaction


def shipping_initial_price(mode, warehouse, wilaya_id, commune_id):
    """ Calculate the initial price of shipping """
    if mode.lower() == "free":
        return 0.00
    with open(settings.SHIPPING_DB, "r", encoding="utf-8") as db_:
        db = json.load(db_)
        # Warehouse wilaya
        _wilaya_ = db['data'][warehouse.name]
        # Get choosen wilaya and retreive it's initial price
        wilaya_cost_shipping = float(_wilaya_[wilaya_id]['initial_price'])
        # Wilaya communes
        _communes_ = _wilaya_[wilaya_id]['communes']
        # Get choosen commune and retreive it's initial price
        commune_cost_shipping = float(_communes_[commune_id]['initial_price'])
    return wilaya_cost_shipping + commune_cost_shipping


def shipping_extra_fees(mode, product):
    if mode.lower() == "free":
        return 0.00
    def calculate_extra(value, max_value, increament_size, increament_value):
        """
        Calculate the extra cost if width, height,length and weight is bigger than the constants values
        """
        final_cost = 0
        if value > max_value:
            extra_value = (value - max_value) / increament_size
            cost = extra_value * increament_value
            final_cost = round(cost, 2)
        return float(final_cost)

    # Constants
    MAX_WIDTH  = 0.65          # m
    WIDTH_INCREASE_SIZE = 0.1  # m
    WIDTH_INCREASE_VALUE = 50  # DA

    MAX_LENGTH = 0.75           # m
    LENGTH_INCREASE_SIZE = 0.1  # m
    LENGTH_INCREASE_VALUE = 60  # DA

    MAX_HEIGHT = 1              # m
    HEIGHT_INCREASE_SIZE = 0.1  # m
    HEIGHT_INCREASE_VALUE = 50  # DA

    MAX_WEIGHT = 5             # kg
    WEIGHT_INCREASE_SIZE  = 1  # kg
    WEIGHT_INCREASE_VALUE = 50 # DA

    # Extra Costs
    extra_width  = calculate_extra(float(product.width), MAX_WIDTH,  WIDTH_INCREASE_SIZE,  WIDTH_INCREASE_VALUE)
    extra_length = calculate_extra(float(product.length), MAX_LENGTH, LENGTH_INCREASE_SIZE, LENGTH_INCREASE_VALUE)
    extra_height = calculate_extra(float(product.height), MAX_HEIGHT, HEIGHT_INCREASE_SIZE, HEIGHT_INCREASE_VALUE)
    extra_weight = calculate_extra(float(product.weight), MAX_WEIGHT, WEIGHT_INCREASE_SIZE, WEIGHT_INCREASE_VALUE)
    # Final Cost
    return extra_width + extra_length + extra_height + extra_weight


def randomize_order_id():
    # Generate orderNumber between 1 and 10M
    return randint(1, 9999999)


def return_items_to_store(bill):
    if bill.status != "Canceled":
        with transaction.atomic():
            for order in bill.orders.all():
                order.product.stock += order.quantity
                order.product.save()
            # then change status to canceled
            bill.status = "Canceled"
            bill.save()