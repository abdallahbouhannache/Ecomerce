# Python
import uuid

def store_logo_path(instance, filename):
    if instance.store_name:
        return f'hangar/store/{instance.store_name}/{filename}'
    return f'hangar/store/products/{instance.first_name}_{instance.last_name}/{filename}'
