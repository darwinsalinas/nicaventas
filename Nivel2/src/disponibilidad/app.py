from flask import jsonify, request
from config import db, create_app
from models import Country, City
import os

db.create_all(app=create_app())
app = create_app()
app.app_context().push()

@app.route('/')
def info():
    info = {
        'id': 'nica-ventas',
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
        "city": city
    }

    country_rs = Country.query.filter(Country.country == country).one_or_none()
    if country_rs is not None:
        city_rs = City.query.filter(City.country_id == country_rs.id).filter(City.city == city).one_or_none()

        if city_rs is not None:
            info['active'] = city_rs.active
            info['country'] = country_rs.country
            info['city'] = city_rs.city

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
            return jsonify(info)
        return page_not_found(404)

    return page_not_found(404)

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
    app.run(debug=True, host='0.0.0.0', port='8000')