import uuid

def thumbs_path(instance, filename):
    if instance.slug is None:
        store_in = str(uuid.uuid4())[0:8]
        return f'hangar/thumbs/products/{filename}'
    return f'hangar/thumbs/products/{filename}'


def product_images_path(instance, filename):
    return f'hangar/images/products/{filename}'