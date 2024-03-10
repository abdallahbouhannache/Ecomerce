# Python
import json
# Django
from django.conf import settings

def load_wilaya(warehouse=None):
    """
    Open DB to get list of wilaya related to a warehouse
    """
    # Open Database file
    with open(settings.SHIPPING_DB, "r", encoding="utf-8") as wilaya_:
        # Check if we want to filter it to fit a warehouse
        if warehouse:
            # Load data
            wilaya = json.load(wilaya_)
            # Break a part the data
            measruing_unit = wilaya['options']['measruing_unit']
            currency = wilaya['options']['currency']
            warehouse_wilaya_ = wilaya['data'][warehouse]
            warehouse_wilaya = [warehouse_wilaya_[x] for x in warehouse_wilaya_]
            # Return it
            return measruing_unit, currency, warehouse_wilaya
        # Or return the object without filtering
        return json.load(wilaya_)

def update_wilaya(distances, prices, warehouse):
    """
    Open DB to set list of wilaya related to a warehouse
    """
    # Load database file
    previous_data = load_wilaya()
    current_wilaya = previous_data['data'][warehouse.name]
    # Update Distances
    for index, value in enumerate(distances, 1):
        # Data -> Warehouse -> Wilaya : Distance Between
        current_wilaya[f"{index}"]['distance_between'] = value
    # Update Prices
    for index, value in enumerate(prices, 1):
        # Data -> Warehouse -> Wilaya : Initial Price
        current_wilaya[f"{index}"]['initial_price'] = value
    # Save changes
    with open(settings.SHIPPING_DB, "w", encoding="utf-8") as wilaya_:
        json.dump(previous_data, wilaya_, ensure_ascii=False, indent=4)
    return 1




def load_communes(warehouse=None, wilaya_id=None):
    """
    Open DB to get list of communes related to a wilaya which is related to a warehouse
    """
    # Open Database file
    with open(settings.SHIPPING_DB, "r", encoding="utf-8") as wilaya_:
        # Check if we want to filter it to fit a warehouse
        if warehouse:
            # Load data
            wilaya = json.load(wilaya_)
            # Break a part the data
            measruing_unit = wilaya['options']['measruing_unit']
            currency = wilaya['options']['currency']
            warehouse_wilaya = wilaya['data'][warehouse][wilaya_id]
            wilaya = {"name":warehouse_wilaya['name'], "ar_name":warehouse_wilaya['ar_name']}
            warehouse_wilaya_communes_ = warehouse_wilaya['communes']
            warehouse_wilaya_communes = [warehouse_wilaya_communes_[x] for x in warehouse_wilaya_communes_]
            # Return it
            return measruing_unit, currency, warehouse_wilaya_communes, wilaya
        # Or return the object without filtering
        return json.load(wilaya_)

def update_communes(distances, prices, warehouse, wilaya_id):
    """
    Open DB to set list of communes related to a wilaya which is related to a warehouse
    """
    # Load database file
    previous_data = load_communes()
    current_wilaya_commune = previous_data['data'][warehouse.name][wilaya_id]['communes']
    ids = [x for x in current_wilaya_commune]
    loop_communes_ids = list(enumerate(ids))
    # Update Distances & Prices
    for index, value in loop_communes_ids:
        # Data -> Warehouse -> Wilaya : Distance Between
        current_wilaya_commune[f"{value}"]['distance_between'] = distances[index]
        current_wilaya_commune[f"{value}"]['initial_price'] = prices[index]
    # Save changes
    with open(settings.SHIPPING_DB, "w", encoding="utf-8") as wilaya_:
        json.dump(previous_data, wilaya_, ensure_ascii=False, indent=4)
    return 1
