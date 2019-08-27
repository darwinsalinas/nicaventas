from flask import Flask, jsonify, request
app = Flask(__name__)

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
    return jsonify(info)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='8000')