# Python
import json
# Django
from django.conf import settings

def populate_wilaya_communes():
    # Read Communes File
    with open(settings.COMMUNES, 'r', encoding='utf-8') as _communes:
        communes = json.load(_communes)
    # Read Wilaya File
    with open(settings.WILAYA, 'r', encoding='utf-8') as _wilaya:
        wilaya = json.load(_wilaya)
    # Refactoring the data
    for key_wilaya in wilaya:
        # Get list of communes of current wilaya
        list_commune = communes[key_wilaya]
        # Append each commune to the the current wilaya
        for commune in list_commune:
            # wilaya_id -> communes - > commune_id
            wilaya[key_wilaya]['communes'][commune['id']] = {
                "id":commune['id'],
                "name":commune['name'],
                "ar_name":commune['ar_name'],
                "distance_between":commune['distance_between'],
                "initial_price":commune['initial_price'],
            }
    # Return Filtred data
    return wilaya



def update_database_json(self):
    with open(settings.SHIPPING_DB, 'r', encoding='utf-8') as _shipping_db:
        # Try to open Database file
        try:
            shipping_db = json.load(_shipping_db)
        # If not possible that mean it's blank
        except Exception as e:
            # Open Schema to initilize database
            with open(settings.SHIPPING_SCHEMA, 'r', encoding='utf-8') as _schema_db:
                shipping_db = json.load(_schema_db)
        # If Create a new warehouse, append Wilaya and Communes to it
        if self.id is None:
            shipping_db['data'][self.name] = populate_wilaya_communes()
        # Otherwise delete Key and replace it with the Key
        else:
            shipping_db['data'][self.name] = shipping_db['data'].pop(self.old_name)
        # Update Database
        with open(settings.SHIPPING_DB, 'w', encoding='utf-8') as new_shipping_db:
            json.dump(shipping_db, new_shipping_db, ensure_ascii=False, indent=4)