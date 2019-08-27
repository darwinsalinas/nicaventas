import os
from config import db, create_app
from models import Product, Rule

db.create_all(app=create_app())
app = create_app()
app.app_context().push()

# Data to initialize database with
PRODUCTS = [
    {
        'sku': 'AZ00001',
        'description': 'Paraguas de señora estampado',
        'price': 10
    },
    {
        'sku': 'AZ00002',
        'description': 'Helado de sabor fresa',
        'price': 1
    }
]

RULES = [
    {
        'city': 'Leon',
        'country': 'ni',
        'sku': 'AZ00001',
        'min_condition': 500,
        'max_condition': 599,
        'variation': 1.5
    },
    {
        'city': 'Leon',
        'country': 'ni',
        'sku': 'AZ00002',
        'min_condition': 500,
        'max_condition': 599,
        'variation': 0.5
    },
    {
        'city': 'Leon',
        'country': 'ni',
        'sku': 'AZ00002',
        'min_condition': 800,
        'max_condition': 810,
        'variation': 1.5
    },
    {
        'city': 'Leon',
        'country': 'ni',
        'sku': 'AZ00001',
        'min_condition': 800,
        'max_condition': 810,
        'variation': 0.5
    },
    {
        'city': 'Managua',
        'country': 'ni',
        'sku': 'AZ00001',
        'min_condition': 500,
        'max_condition': 599,
        'variation': 1.5
    },
    {
        'city': 'Managua',
        'country': 'ni',
        'sku': 'AZ00002',
        'min_condition': 500,
        'max_condition': 599,
        'variation': 0.5
    },
    {
        'city': 'Managua',
        'country': 'ni',
        'sku': 'AZ00002',
        'min_condition': 800,
        'max_condition': 810,
        'variation': 1.5
    },
    {
        'city': 'Managua',
        'country': 'ni',
        'sku': 'AZ00001',
        'min_condition': 800,
        'max_condition': 810,
        'variation': 0.5
    },
    {
        'city': 'Chinandega',
        'country': 'ni',
        'sku': 'AZ00001',
        'min_condition': 500,
        'max_condition': 599,
        'variation': 1.5
    },
    {
        'city': 'Chinandega',
        'country': 'ni',
        'sku': 'AZ00002',
        'min_condition': 500,
        'max_condition': 599,
        'variation': 0.5
    },
    {
        'city': 'Chinandega',
        'country': 'ni',
        'sku': 'AZ00002',
        'min_condition': 800,
        'max_condition': 810,
        'variation': 1.5
    },
    {
        'city': 'Chinandega',
        'country': 'ni',
        'sku': 'AZ00001',
        'min_condition': 800,
        'max_condition': 810,
        'variation': 0.5
    },
    {
        'city': 'Bluefields',
        'country': 'ni',
        'sku': 'AZ00001',
        'min_condition': 500,
        'max_condition': 599,
        'variation': 1.5
    },
    {
        'city': 'Bluefields',
        'country': 'ni',
        'sku': 'AZ00002',
        'min_condition': 500,
        'max_condition': 599,
        'variation': 0.5
    },
    {
        'city': 'Bluefields',
        'country': 'ni',
        'sku': 'AZ00002',
        'min_condition': 800,
        'max_condition': 810,
        'variation': 1.5
    },
    {
        'city': 'Bluefields',
        'country': 'ni',
        'sku': 'AZ00001',
        'min_condition': 800,
        'max_condition': 810,
        'variation': 0.5
    },
    {
        'city': 'Nueva Guinea',
        'country': 'ni',
        'sku': 'AZ00001',
        'min_condition': 500,
        'max_condition': 599,
        'variation': 1.5
    },
    {
        'city': 'Nueva Guinea',
        'country': 'ni',
        'sku': 'AZ00002',
        'min_condition': 500,
        'max_condition': 599,
        'variation': 0.5
    },
    {
        'city': 'Nueva Guinea',
        'country': 'ni',
        'sku': 'AZ00002',
        'min_condition': 800,
        'max_condition': 810,
        'variation': 1.5
    },
    {
        'city': 'Nueva Guinea',
        'country': 'ni',
        'sku': 'AZ00001',
        'min_condition': 800,
        'max_condition': 810,
        'variation': 0.5
    }
]
# Create the database
db.create_all()

# Iterate over the PEOPLE structure and populate the database
for product in PRODUCTS:
    p = Product(sku=product['sku'], description=product['description'], price=product['price'])
    db.session.add(p)

db.session.commit()

for rule in RULES:
    r = Rule(
            city=rule['city'],
            country=rule['country'],
            sku=rule['sku'],
            min_condition=rule['min_condition'],
            max_condition=rule['max_condition'],
            variation=rule['variation']
        )
    db.session.add(r)

db.session.commit()