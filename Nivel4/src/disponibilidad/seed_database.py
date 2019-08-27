from config import db, create_app
from models import Country, City

db.create_all(app=create_app())
app = create_app()
app.app_context().push()

# Data to initialize database with
COUNTRIES = [
    {'country': 'ni'}
]

CITIES = [
    {'city': 'Leon', 'active': True, 'country_id': 1},
    {'city': 'Chinandega', 'active': True, 'country_id': 1},
    {'city': 'Matagalpa', 'active': True, 'country_id': 1},
    {'city': 'Managua', 'active': True, 'country_id': 1},
    {'city': 'Granada', 'active': True, 'country_id': 1},
]

# Create the database
db.create_all()

# Iterate over the PEOPLE structure and populate the database
for country in COUNTRIES:
    c = Country(country=country['country'])
    db.session.add(c)

db.session.commit()

for city in CITIES:
    cc = City(city=city['city'], active=city['active'],country_id=city['country_id'])
    db.session.add(cc)

db.session.commit()