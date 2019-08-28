from flask import jsonify, request, escape
from config import db, r, create_app
from models import Country, City
import os

app = create_app()
app.app_context().push()

@app.route('/')
def info():
    info = {
        'id': 'nica-ventas-disponibilidad',
        'version': '0.1',
        'status': 'development'
    }
    return jsonify(info)

@app.route('/active')
def city_is_active():
    country = request.args.get("country", "ni")
    city = request.args.get("city", "Managua")
    info = {
        "active": False,
        "country": country,
        "city": city,
        'cache': 'hit'
    }
    in_cache = get_from_cache(country, city)
    if in_cache:
        info['active'] = bool(in_cache == b'1')
        return jsonify(info)

    country_rs = Country.query.filter(Country.country == country).one_or_none()
    if country_rs is not None:
        city_rs = City.query.filter(City.country_id == country_rs.id).filter(City.city == city).one_or_none()

        if city_rs is not None:
            info['active'] = city_rs.active
            info['country'] = country_rs.country
            info['city'] = city_rs.city
            info['cache'] = 'miss'
            store_on_cache(country_rs.country, city_rs.city, city_rs.active)

    return jsonify(info)

@app.route('/active', methods=['POST'])
def store_city():
    country = request.json.get("country", "ni")
    city = request.json.get("city", "Managua")
    active = request.json.get("active", False)
    country_rs = Country.query.filter(Country.country == country).one_or_none()

    if country_rs is not None:
        city_rs = City.query.filter(City.country_id == country_rs.id).filter(City.city == city).one_or_none()

        if city_rs is None:
            city_rs = City(city=city, active=active,country_id=country_rs.id)
            db.session.add(city_rs)
            db.session.commit()

    else:
        country_rs = Country(country=country)
        db.session.add(country_rs)
        db.session.commit()

        city_rs = City(city=city, active=active,country_id=country_rs.id)
        db.session.add(city_rs)
        db.session.commit()

    info = {
        "active": active,
        "country": country,
        "city": city
    }
    delete_all_from_cache()
    return jsonify(info)

@app.route('/active', methods=['PUT', 'PATCH'])
def update_city():
    token = request.headers.get('Authorization', False)
    if (token != "Bearer " + os.environ['TOKEN']):
        return not_allowed(403)

    country = request.json.get("country", "ni")
    city = request.json.get("city", "Managua")
    active = request.json.get("active", False)

    country_rs = Country.query.filter(Country.country == country).one_or_none()
    if country_rs is not None:
        city_rs = City.query.filter(City.country_id == country_rs.id).filter(City.city == city).one_or_none()

        if city_rs is not None:
            city_rs.active = active
            db.session.commit()

            info = {
                "active": active,
                "country": country,
                "city": city
            }
            delete_all_from_cache()
            return jsonify(info)
        return page_not_found(404)

    return page_not_found(404)

def store_on_cache(country, city, data):
    chache_name = create_cache_name(country, city)
    value = 0
    if data:
        value = 1
    r.set(escape(chache_name), value)

def get_from_cache(country, city):
    chache_name = create_cache_name(country, city)
    data = r.get(escape(chache_name))
    return data

def delete_from_cache(country, city):
    chache_name = create_cache_name(country, city)
    r.delete(escape(chache_name))

def delete_all_from_cache():
    keys = r.keys('*')
    for k in keys:
        print('Deleting:', k, 'result is')
        r.delete(k)

def create_cache_name(country, city):
    cache_name = '{0}_{1}'.format(country, city)
    return cache_name

@app.errorhandler(404)
def page_not_found(e):
    info = {
        'app-id': 'nica-ventas-disponibilidad',
        'version': '0.1',
        'status': 'development',
        "title": "Error 404, Not Found",
        "detail": "Error 404, Not Found",
        "message": "Erorr 404, Not Found",
        "status": 404,
        "code": 404
    }

    return jsonify(info)

@app.errorhandler(403)
def not_allowed(e):
    info = {
        'app-id': 'nica-ventas-disponibilidad',
        'version': '0.1',
        'status': 'development',
        "title": "Error 403, Forbidden",
        "detail": "Error 403, Forbidden",
        "message": "Erorr 403, Forbidden",
        "status": 403,
        "code": 403
    }

    return jsonify(info)

if __name__ == '__main__':
    dbstatus = False
    while dbstatus == False:
        try:
            db.create_all()
        except:
            time.sleep(2)
        else:
            dbstatus = True
    app.run(debug=True, host='0.0.0.0', port='8000')