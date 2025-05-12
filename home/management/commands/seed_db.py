import os
import random
import requests
from django.core.files import File
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from faker import Faker
from home.models import Category, Product
from store.models import Store
from membership.models import Member
from shipping.models import Warehouse
from django.contrib.auth.models import User
from io import BytesIO
from django.conf import settings


import time
from unsplash import download_unsplash_image

fake = Faker()


class Command(BaseCommand):
    help = 'Populate the database with fake data for presentation'
    

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting database population...\n")
        products_dir = os.path.join(settings.MEDIA_ROOT, "products")
        os.makedirs(products_dir, exist_ok=True)

        # Create categories
        categories = ['Electronics', 'Fashion', 'Home Appliances', 'Books', 'Toys']
        for category_name in categories:
            Category.objects.create(
                en_name=category_name,
                fr_name=f"Catégorie {category_name}",
                ar_name=f"فئة {category_name}",
                icon="fa-box"
            )

        # Create stores
        for _ in range(5):
            user = User.objects.create_user(
                username=fake.user_name(),
                email=fake.email(),
                password='password123'
            )
            Store.objects.create(
                owner=user,
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                store_name=fake.company(),
                nif=fake.ssn(),
                register_commerce=fake.uuid4(),
                active=True,
                verified=True
            )

        # Create warehouses
        for _ in range(3):
            Warehouse.objects.create(
                name=fake.company(),
                address=fake.address()
            )

        # Create products
        categories = Category.objects.all()
        stores = Store.objects.all()
        warehouses = Warehouse.objects.all()
        for _ in range(20):
            category = random.choice(categories)
            store = random.choice(stores)
            warehouse = random.choice(warehouses)
            product = Product.objects.create(
                en_name=fake.word(),
                fr_name=fake.word(),
                ar_name=fake.word(),
                category=category,
                store=store,
                warehouse=warehouse,
                stock=random.randint(1, 100),
                current_price=random.uniform(10.0, 500.0),
                commission=random.uniform(1.0, 50.0),
                rating=random.randint(1, 5),
                length=random.uniform(0.1, 2.0),
                width=random.uniform(0.1, 2.0),
                height=random.uniform(0.1, 2.0),
                weight=random.uniform(0.1, 5.0),
                created_date=fake.date_this_decade()
            )
            # Download and assign a product image
            # img_url = "https://www.freepik.com/free-photo/wooden-table-with-cactus_1150-12345.jpg"  # Replace with actual image URL
            try:
                # pathpic=f"{product.en_name}.jpg"
                # img_data=download_unsplash_image(product.en_name,pathpic )

                # pathpic = os.path.join(settings.MEDIA_ROOT, f"{product.en_name}.jpg")
                pathpic = os.path.join(products_dir, f"{product.en_name}.jpg")

                img_data = download_unsplash_image(product.en_name, pathpic)

                img_name = f"{slugify(product.en_name)}.jpg"
                # img_data = requests.get(img_url).content
                img_file = BytesIO(img_data.content)
                product.thumbnail.save(img_name, File(img_file), save=True)

                product.show= True
                product.save(update_fields=["show"])
            except Exception as e:
                pass

            time.sleep(1)  # Pause execution for 5 seconds


        self.stdout.write(self.style.SUCCESS("Database populated successfully!"))
