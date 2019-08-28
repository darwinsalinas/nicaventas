from flask import jsonify, request, escape
from config import db, r, create_app
import os, requests, json
from models import Product, Rule

app = create_app()
app.app_context().push()

@app.route('/')
def info():
    info = {
        'id': 'nica-ventas-condiciones',
        'version': '0.1',
        'status': 'development'
    }
    return jsonify(info)

@app.route('/price/<sku>') # /price/<:sku>
def get_price(sku):
    producto_rs = Product.query.filter(Product.sku == sku).one_or_none()
    if producto_rs is not None:
        producto = {
            "description": producto_rs.description,
            "price": producto_rs.price
        }
        return jsonify(producto)

    return page_not_found(404)

@app.route('/quote', methods=['POST'])
def get_quote():
    country = request.json.get("country", False)
    city = request.json.get("city", False)
    sku = request.json.get("sku", False)

    if country and city and sku:
        in_cache = get_from_cache(country, city, sku)
        if in_cache:
            data_json = json.loads(in_cache)
            data_json['cache'] = 'hit'
            return jsonify(data_json)

        weather_id = get_weather_id(country, city)
        rule = get_rule(country, city, sku, weather_id)

        variation = 1
        if rule is not None:
            variation = rule.variation

        producto_rs = Product.query.filter(Product.sku == sku).one_or_none()

        resp = {
            "sku": sku,
            "description": producto_rs.description,
            "country": country,
            "city": city,
            "base_price": producto_rs.price,
            "variation": variation,
            "cache": 'miss'
        }
        store_on_cache(country, city, sku, resp)
        return jsonify(resp)

    return page_not_found(404)

def get_rule(country, city, sku, weather_id):
    rule = Rule.query.filter(Rule.country == country)\
        .filter(Rule.city == city)\
        .filter(weather_id >= Rule.min_condition )\
        .filter(weather_id  <= Rule.max_condition)\
        .filter(Rule.sku == sku)\
        .order_by(Rule.id.desc()) \
        .first()

    return rule

def get_weather_id(country, city):
    url = create_url(country, city)
    response = requests.get(url)
    weather_id = 0
    if response.status_code == 200:
        weather_json = response.json()
        weather_id = weather_json['weather'][0]['id']

    return weather_id

def create_url(country, city):
    url_base = 'http://api.openweathermap.org'
    api_version = 'data/2.5/weather'
    api_key = app.config['API_KEY_OWM']
    url = '{0}/{1}?q={2},{3}&APPID={4}&units=metric'.format(
        url_base,
        api_version,
        city,
        country,
        api_key
    )
    return url

def store_on_cache(country, city, sku, data):
    chache_name = create_cache_name(country, city, sku)
    value = json.dumps(data)
    r.set(escape(chache_name), value, ex=300)

def get_from_cache(country, city, sku,):
    chache_name = create_cache_name(country, city, sku)
    data = r.get(escape(chache_name))
    return data

def delete_from_cache(country, city, sku):
    chache_name = create_cache_name(country, city, sku)
    r.delete(escape(chache_name))

def delete_all_from_cache():
    keys = r.keys('*')
    for k in keys:
        print('Deleting:', k, 'result is')
        r.delete(k)

def create_cache_name(country, city, sku):
    cache_name = '{0}_{1}_{2}'.format(country, city, sku)
    return cache_name

@app.errorhandler(404)
def page_not_found(e):
    info = {
        'app-id': 'nica-ventas-condiciones',
        'version': '0.1',
        'status': 'development',
        "title": "Error 404, Not Found",
        "detail": "Error 404, Not Found",
        "message": "Erorr 404, Not Found",
        "status": 404,
        "code": 404
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
    app.run(debug=True, host='0.0.0.0', port='5001')