# Nivel 4

### Descripción general
La aplicación de NicaVentas cuenta con dos micro servicios con una estructura bastante simple, los cuales fueron creados para interactuar con el servicio de base de datos(postgres) y el servicio de caché(redis), el primero de estos dos servicios es el servicio de consulta de disponibilidad de ventas por país y ciudades, el segundo es el servicio de consulta de condiciones de venta, en este segundo servicio se hace uso del API de **OpenWeatherMaps** para consultar el estado del clima en el Pais y ciudad solicitado, esto con el fin de poder hacer una venta diferenciada de acuerdo al clima que se esté presentado en ese momento en la ciudad.

#### Estructura de carpetas y archivos para la aplicación NicaVentas:

```bash
src
├── condiciones
│   ├── Dockerfile
│   ├── __pycache__
│   ├── app.py
│   ├── config.py
│   ├── migrations
│   ├── models.py
│   ├── requirements.txt
│   └── seed_database.py
├── disponibilidad
│   ├── Dockerfile
│   ├── __pycache__
│   ├── app.py
│   ├── config.py
│   ├── models.py
│   ├── requirements.txt
│   └── seed_database.py
├── docker-compose.yml
└── initdb.sql
```

## Servicio de consulta de disponibilidad de ventas

Servicio web se emplea para consultar si se está autorizada la venta de productos en general en una ciudad concreta de un país haciendo uso del endpoint `[GET] /active?city=leon&country=ni`.

El resultado de la invocación de este endpoint, a modo de ejemplo, será el siguiente:

```json
{
  "active": true,
  "country": "ni",
  "city": "Leon"
}
```


El campo `active` indica si la venta está autorizada (`true`) o no (`false`) en la correspondiente ciudad (`city`) del país (`country`) especificado en la llamada.

Una serie de operadores son los encargados de activar y desactivar las posibilidades de venta en las ciudades. Estos operadores disponen del siguiente endpoint del API para activar o desactivar la venta:


Modificar el estado de actividad de una ciudad de un país:
**URL**: `/active`
**Method**: `PUT`
**Auth required**: YES
**Body format**: `Content-type: application/json`
**Body payload**:
```
{
  "active": true,
  "country": "ni",
  "city": "Leon"
}
```


Esta llamada solo se atenderá si incluye en las cabeceras HTTP un token de autenticación como el siguiente:

`Authorization: Bearer 2234hj234h2kkjjh42kjj2b20asd6918`

## Servicio de consulta de condiciones de venta

El servicio de condiciones de venta permite consultar qué porcentaje de descuento se hará a un producto determinado. Los productos se identifican mediante un código único denominado SKU. A modo de ejemplo vamos a considerar dos productos:

|   SKU   |          DESCRIPCION         | PRECIO |
|:-------:|:-----------------------------|-------:|
| AZ00001 | Paraguas de señora estampado |    10€ |
| AZ00002 | Helado de sabor fresa        |     1€ |

El precio final de venta dependerá de dos factores: la ciudad y país de venta, y la condiciones meteorológicas de esa ciudad. La idea general es vender más caros los paraguas y más baratos los helados si estuviera lloviendo, y al contrario, abaratar los paraguas y encarecer helados si hiciera sol. Se proporcionará para esta consulta el endpoint `[GET] /price/<:sku>`.

Por ejemplo, si la venta se hace en León (Nicaragua) y está lloviendo en ese momento, la llamada `[POST] /quote` con body:
```
{
  "sku": "AZ00001",
  "country": "ni",
  "city": "Leon"
}
```
Respondería, por ejemplo:

```
{
  "sku": "AZ00001",
  "description": "Paraguas de señora estampado",
  "country": "ni",
  "city": "Leon",
  "base_price": 10,
  "variation": 1.5
}
```

El precio de los paraguas bajo estas condiciones sería de `10 x 1.5 = 15€`.

Para calcular la respuesta adecuada, el endpoint `[POST] /quote` dispondrá del API de un tercero, concretamente de **OpenWeather**, para consultar el tiempo meteorológico de una ciudad concreta de un país.

Con la información devuelta por el API de **OpenWeather** estamos en condiciones de comparar con las reglas de variación que hayamos creado en la base de datos:


| id_regla | ciudad | pais |     SKU | min_condition | max_condition | variation |
|---------:|-------:|-----:|--------:|--------------:|--------------:|----------:|
|        1 |   Leon |   NI | AZ00001 |           500 |           599 |       1.5 |
|        2 |   Leon |   NI | AZ00002 |           500 |           599 |       0.5 |
|          |        |      |         |               |               |           |

Supongamos que preguntamos al servicio meteorológico sobre las condiciones en Leon, Nicaragua, y obtenemos id=503 (very heavy rain). Consultamos a continuación a la base de datos y si se cumple al menos una regla de las que tengamos guardadas entonces el valor de `variation` será la variación que debemos usar. Si por el contrario no se cumpliera ninguna regla se podría considerar que la variación es 1, o lo que es lo mismo, que no hay variación.


## Procedimiento realizado para la creación y publicación de las imágenes de Docker
- URL de dockerhub del [servicio de consulta de disponibilidad](https://cloud.docker.com/repository/docker/darwinsalinas/nicaventas-disponibilidad-nivel4)

- URL de dockerhub del [servicio de consulta de condiciones de venta](https://cloud.docker.com/repository/docker/darwinsalinas/nicaventas-condiciones-nivel4)

Para crear una imagen de Docker que pueda correr el código de nuestros Micro servicios realizados con Flask se utilizó una imagen oficial de Docker para Python:

- URL de [imagen de Python](https://hub.docker.com/_/python)

Esta imagen contiene lo necesario para correr código de Python, por lo cual a partir de ella se ha creado la imagen que contiene el código del Micro servicio, para reproducir una imagen igual a la que se ha creado debemos escribir el siguiente código en nuestro archivo Dockerfile:

```
FROM python
LABEL maintainer "Darwin Salinas <salinash2000@gmail.com>"
RUN mkdir /app
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.2.1/wait /wait
RUN chmod +x /wait
CMD /wait && python app.py
```

Puedes reemplazar el nombre y correo del `manteiner` de la imagen

Para construir las imágenes de Docker y etiquetarlas ejecutamos esta línea en terminal dentro de la carpeta correspondiente de cada micro servicio:

```bash
docker build -t darwinsalinas/nicaventas-disponibilidad-nivel4 .
docker build -t darwinsalinas/nicaventas-condiciones-nivel4 .
```


Para subir nuestras imágenes recién creadas ejecutamos lo siguiente en terminal:

```bash
docker login && docker push darwinsalinas/nicaventas-condiciones-nivel4
docker login && docker push darwinsalinas/nicaventas-disponibilidad-nivel4
```

Al ejecutar las lineas de arriba se nos va a solicitar nuestras credenciales de dockerhub.


Para correr los servicios orquestados con docker-compose se requiere la presencia de un archivo de entorno `.env` que contenga todas las credenciales y configuraciones de la aplicación:

```bash
POSTGRES_DB=nicaventas
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_PORT=5432
DB_SERVICE=nicaventas-db
APP_SETTINGS=config.DevelopmentConfig
FLASK_DEBUG=1
TOKEN=2234hj234h2kkjjh42kjj2b20asd6918
REDIS_PORT=6379
REDIS_LOCATION=redis
API_KEY_OWM=3d3ea700fcb655178274e26b3af34ccd
```

Aparte del archivo de configuración anteriormente descrito, también necesitamos el script de `initdb.sql` para crear las tablas y rellenarla con datos para realizar pruebas:

```SQL
CREATE TABLE "public"."countries" (
  "id" serial,
  "country" varchar(128) COLLATE "pg_catalog"."default",
  CONSTRAINT "countries_pkey" PRIMARY KEY ("id"),
  CONSTRAINT "countries_country_key" UNIQUE ("country")
);

CREATE TABLE "public"."cities" (
  "id" serial,
  "city" varchar(128) COLLATE "pg_catalog"."default",
  "active" bool,
  "country_id" int4,
  CONSTRAINT "cities_pkey" PRIMARY KEY ("id"),
  CONSTRAINT "cities_country_id_fkey" FOREIGN KEY ("country_id") REFERENCES "public"."countries" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION
);

CREATE TABLE "public"."products" (
  "id" serial,
  "sku" varchar(128) COLLATE "pg_catalog"."default",
  "description" varchar(128) COLLATE "pg_catalog"."default",
  "price" float8,
  CONSTRAINT "products_pkey" PRIMARY KEY ("id"),
  CONSTRAINT "products_sku_key" UNIQUE ("sku")
);

CREATE TABLE "public"."rules" (
  "id" serial,
  "country" varchar(128) COLLATE "pg_catalog"."default",
  "city" varchar(128) COLLATE "pg_catalog"."default",
  "sku" varchar(128) COLLATE "pg_catalog"."default",
  "min_condition" int4,
  "max_condition" int4,
  "variation" float8,
  CONSTRAINT "rules_pkey" PRIMARY KEY ("id")
);

INSERT INTO "public"."countries"("id", "country") VALUES (1, 'ni');
INSERT INTO "public"."cities"("city", "active", "country_id") VALUES ('Leon', 't', 1);
INSERT INTO "public"."cities"("city", "active", "country_id") VALUES ('Chinandega', 't', 1);
INSERT INTO "public"."cities"("city", "active", "country_id") VALUES ('Matagalpa', 't', 1);
INSERT INTO "public"."cities"("city", "active", "country_id") VALUES ('Managua', 't', 1);
INSERT INTO "public"."cities"("city", "active", "country_id") VALUES ('Granada', 't', 1);

INSERT INTO "public"."products"("sku", "description", "price") VALUES ('AZ00001', 'Paraguas de señora estampado', 10);
INSERT INTO "public"."products"("sku", "description", "price") VALUES ('AZ00002', 'Helado de sabor fresa', 1);

INSERT INTO "public"."rules"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Leon', 'AZ00001', 500, 599, 1.5);
INSERT INTO "public"."rules"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Leon', 'AZ00002', 500, 599, 0.5);
INSERT INTO "public"."rules"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Leon', 'AZ00002', 800, 810, 1.5);
INSERT INTO "public"."rules"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Leon', 'AZ00001', 800, 810, 0.5);
INSERT INTO "public"."rules"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Managua', 'AZ00001', 500, 599, 1.5);
INSERT INTO "public"."rules"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Managua', 'AZ00002', 500, 599, 0.5);
INSERT INTO "public"."rules"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Managua', 'AZ00002', 800, 810, 1.5);
INSERT INTO "public"."rules"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Managua', 'AZ00001', 800, 810, 0.5);
INSERT INTO "public"."rules"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Chinandega', 'AZ00001', 500, 599, 1.5);
INSERT INTO "public"."rules"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Chinandega', 'AZ00002', 500, 599, 0.5);
INSERT INTO "public"."rules"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Chinandega', 'AZ00002', 800, 810, 1.5);
INSERT INTO "public"."rules"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Chinandega', 'AZ00001', 800, 810, 0.5);
INSERT INTO "public"."rules"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Bluefields', 'AZ00001', 500, 599, 1.5);
INSERT INTO "public"."rules"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Bluefields', 'AZ00002', 500, 599, 0.5);
INSERT INTO "public"."rules"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Bluefields', 'AZ00002', 800, 810, 1.5);
INSERT INTO "public"."rules"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Bluefields', 'AZ00001', 800, 810, 0.5);
INSERT INTO "public"."rules"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Nueva Guinea', 'AZ00001', 500, 599, 1.5);
INSERT INTO "public"."rules"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Nueva Guinea', 'AZ00002', 500, 599, 0.5);
INSERT INTO "public"."rules"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Nueva Guinea', 'AZ00002', 800, 810, 1.5);
INSERT INTO "public"."rules"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Nueva Guinea', 'AZ00001', 800, 810, 0.5);
INSERT INTO "public"."rules"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Juigalpa', 'AZ00001', 500, 599, 1.5);
INSERT INTO "public"."rules"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Juigalpa', 'AZ00002', 500, 599, 0.5);
INSERT INTO "public"."rules"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Juigalpa', 'AZ00002', 800, 810, 1.5);
INSERT INTO "public"."rules"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Juigalpa', 'AZ00001', 800, 810, 0.5);
INSERT INTO "public"."rules"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Rivas', 'AZ00001', 500, 599, 1.5);
INSERT INTO "public"."rules"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Rivas', 'AZ00002', 500, 599, 0.5);
INSERT INTO "public"."rules"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Rivas', 'AZ00002', 800, 810, 1.5);
INSERT INTO "public"."rules"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Rivas', 'AZ00001', 800, 810, 0.5);
```

### El archivo dcoker-compose
Para poner en funcionamiento los dos micro servicios, mas la base de datos y el servicio de cache con un solo comando, en este ejemplo se hace uso del orquestador Docker compose, compose utiliza un archivo YML para configurar y arrancar los servicios de la aplicación.

A continuación las lineas necesarias en el archivo `docker-compose.yml`
```bash
version: '3'
services:
  nicaventas-db:
    restart: always
    image: postgres
    container_name: "nicaventas-db"
    env_file:
      - .env
    ports:
      - "54320:5432"
    volumes:
      - ./initdb.sql:/docker-entrypoint-initdb.d/initdb.sql
    # volumes:
    #   - my_dbdata:/var/lib/postgresql/data

  nicaventas-disponibilidad:
    restart: always
    depends_on:
      - nicaventas-db
    environment:
      WAIT_HOSTS: nicaventas-db:5432
    container_name: "nicaventas-disponibilidad-us"
    image: darwinsalinas/nicaventas-disponibilidad-nivel4
    env_file:
    - .env
    ports:
      - 5000:5000
    command: flask run --host=0.0.0.0

  nicaventas-condiciones:
    restart: always
    depends_on:
      - nicaventas-db
    environment:
      WAIT_HOSTS: nicaventas-db:5432
    container_name: "nicaventas-condiciones-us"
    image: darwinsalinas/nicaventas-condiciones-nivel4
    env_file:
    - .env
    ports:
      - 5001:5000
    command: flask run --host=0.0.0.0

  redis:
    image: redis
    expose:
      - 6379

volumes:
  my_dbdata:
```

Ya con estos archivos podemos correr nuestros servicios con la siguiente instrucción:

```bash
docker-compose up
```

Si queremos poner a correr ls servicios en segundo plano podemos agregarle el flag `-d`:
```bash
docker-compose up -d
```

Si pusiste los servicios en segundo plano puedes ver lo que ocurre dentro de los contenedores con el comando:

```bash
docker logs -f nicaventas-db
```



## Probar el funcionamiento de los micro servicios

### Servicio de consulta de disponibilidad de venta

Probar con Postman, el navegador o también lo puedes hacer con: `curl localhost:5000/active?city=leon&country=ni`. La respuesta que devuelve debe ser una respuesta JSON como esto:
```bash
[1] 12962
{
  "active": false,
  "cache": "hit",
  "city": "leon",
  "country": "ni"
}
[1]  + 12962 done       curl localhost:5000/active?city=leon
```

Para `guardar` un nuevo registro en la base de datos podemos ejecutar esta linea en la terminal:
```bash
curl -X POST -d '{"city":"ElRama","country":"ni","active":true}' -H "Content-Type: application/json" localhost:5000/active
```
Esto nos debe responder un json con los datos del registro que ha sido guardado:
```JSON
{
  "active": true,
  "city": "ElRama",
  "country": "ni"
}
```

Si queremos comprobar que realmente se ha guardado en la base de datos podemos usar esta linea en la terminal:
```bash
curl localhost:5000/active?city=ElRama&country=ni
```
La petición anterior nos devolverá el registro con los datos solicitados:
```bash
[1] 4620
{
  "active": true,
  "cache": "miss",
  "city": "ElRama",
  "country": "ni"
}
[1]  + 4620 done       curl localhost:5000/active?city=ElRama
```

Si nos fijamos con detenimiento, en este caso la respuesta incluye un atributo llamado `"cache": "miss"` lo cual nos indica que la petición realizada ha llegado hasta la base de datos, pero si volvemos a hacer la misma petición veremos que ahora se nos devuelve el siguiente json con el atributo `"cache": "hit"` indicando que ahora los datos provienen de la cache, optimizando los tiempos de carga:
```bash
[1] 8309
{
  "active": true,
  "cache": "hit",
  "city": "ElRama",
  "country": "ni"
}
[1]  + 8309 done       curl localhost:5000/active?city=ElRama
```

Para `actualizar` un registro podemos ejecutar la siguiente linea en terminal:
```bash
curl -X PUT -d '{"city":"El Rama","country":"ni","active":false}' -H "Content-Type: application/json" -H "Authorization: Bearer 2234hj234h2kkjjh42kjj2b20asd6918" localhost:5000/active
```
Como se puede notar, para lograr esta petición con éxito es necesario que junto con los datos enviado se mande también el token de autorización, de lo contrario la petición devolverá un error, Si la petición se ejecuta sin problemas nos devuelve un json con el registro actualizado:
```JSON
{
  "active": false,
  "city": "ElRama",
  "country": "ni"
}
```
En caso de error de autorización nos devuelve:
```bash
{
  "app-id": "nica-ventas-disponibilidad",
  "code": 403,
  "detail": "Error 403, Forbidden",
  "message": "Erorr 403, Forbidden",
  "status": 403,
  "title": "Error 403, Forbidden",
  "version": "0.1"
}
```


Si queremos estar totalmente seguros de que se ha actualizado en la base de datos podemos usar esta linea en la terminal:
```bash
curl localhost:5000/active?city=ElRama&country=ni
```
Ademas de devolvernos el registro actualizado, ahora veremos que también la cache ha sido borrada y se hizo la consulta en base de datos, tal como se nos indica con ` "cache": "miss"`:
```bash
[1] 18146
{
  "active": false,
  "cache": "miss",
  "city": "ElRama",
  "country": "ni"
}
[1]  + 18146 done       curl localhost:5000/active?city=ElRama
```


### Servicio de consulta de condiciones de venta
Como se mencionó al principio, este servicio tiene la particularidad que hace uso del API de **OpenWeather** para consultar el estado del clima de la ciudad donde se quiere realizar la venta, primeramente para este servicio tenemos disponible una ruta para consultar directamente el precio base de un producto del inventario:

```bash
curl http://127.0.0.1:5001/price/AZ00001
```

Con los datos de pruebas que hemos insertado en la base de datos tenemos disponibles 2 artículos para consultar por medio de su SKU, el AZ00001 y el AZ00002.

Al ejecutar la petición anterior se nos debe devolver un json similar a esto:
```JSON
{
  "description": "Paraguas de señora estampado",
  "price": 10
}
```

Para consultar la variación de precio de acuerdo al estado del clima en la ciudad donde se quiere realizar la venta podemos usar esta linea en la terminal:
```bash
curl -X POST -d '{"city":"Leon","country":"ni","sku":"AZ00001"}' -H "Content-Type: application/json" http://127.0.0.1:5001/quote
```
Si al momento de realizar la petición está lloviendo en la ciudad y país especificado entonces obtendremos una variación que nos permita vender mas caro los paraguas, al momento en el que se realizó la petición no estaba lloviendo en León por lo que el servicio me devuelve esta respuesta:
```bash
{
  "base_price": 10.0,
  "cache": "miss",
  "city": "Leon",
  "country": "ni",
  "description": "Paraguas de se\u00f1ora estampado",
  "sku": "AZ00001",
  "variation": 0.5
}
```
Esto nos indica que deberíamos vender los paraguas mas baratos, pero si hacemos la misma petición para los Helados con la siguiente linea:

```bash
curl -X POST -d '{"city":"Leon","country":"ni","sku":"AZ00002"}' -H "Content-Type: application/json" http://127.0.0.1:5001/quote
```

Ahora vemos que el producto solicitado para el país y ciudad debe venderse mas caro, de acuerdo al clima de ese momento:
```bash
{
  "base_price": 1.0,
  "cache": "miss",
  "city": "Leon",
  "country": "ni",
  "description": "Helado de sabor fresa",
  "sku": "AZ00002",
  "variation": 1.5
}
```

## Construcción de los micro servicios
Los servicios para el API fueron creados usando `Python` y `Flask` y algunas librerías de Python como Flask-SQLAlchemy, requests, redis, a continuación el código fuente de Python para cada uno de los micro servicios

### Servicio de consulta de disponibilidad

app.py
```python
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
```

config.py
```python
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import redis

class Config(object):
    DEBUG = False
    TESTING = False
    DB_NAME = os.environ['POSTGRES_DB']
    DB_USER = os.environ['POSTGRES_USER']
    DB_PASS = os.environ['POSTGRES_PASSWORD']
    DB_SERVICE = os.environ['DB_SERVICE']
    DB_PORT = os.environ['DB_PORT']
    SQLALCHEMY_DATABASE_URI = 'postgresql://{0}:{1}@{2}:{3}/{4}'.format(
        DB_USER, DB_PASS, DB_SERVICE, DB_PORT, DB_NAME
    )

class ProductionConfig(Config):
    DEBUG = False

class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

basedir = os.path.abspath(os.path.dirname(__file__))

db = SQLAlchemy()
def create_app():
    app = Flask(__name__)
    app.config.from_object(os.environ['APP_SETTINGS'])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    return app

r = redis.Redis(host=os.environ['REDIS_LOCATION'], port=os.environ['REDIS_PORT'], db=0)
```

models.py
```python
from datetime import datetime
from config import db


class Country(db.Model):
    __tablename__ = 'countries'
    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(128), unique=True)

class City(db.Model):
    __tablename__ = 'cities'
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(128))
    active = db.Column(db.Boolean)
    country_id = db.Column(db.Integer, db.ForeignKey('countries.id'))
```

### Servicio de consulta condiciones de venta

app.py
```python
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
```

config.py
```python
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import redis

class Config(object):
    DEBUG = False
    TESTING = False
    API_KEY_OWM = os.environ['API_KEY_OWM']
    DB_NAME = os.environ['POSTGRES_DB']
    DB_USER = os.environ['POSTGRES_USER']
    DB_PASS = os.environ['POSTGRES_PASSWORD']
    DB_SERVICE = os.environ['DB_SERVICE']
    DB_PORT = os.environ['DB_PORT']
    SQLALCHEMY_DATABASE_URI = 'postgresql://{0}:{1}@{2}:{3}/{4}'.format(
        DB_USER, DB_PASS, DB_SERVICE, DB_PORT, DB_NAME
    )

class ProductionConfig(Config):
    DEBUG = False

class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

basedir = os.path.abspath(os.path.dirname(__file__))

db = SQLAlchemy()
def create_app():
    app = Flask(__name__)
    app.config.from_object(os.environ['APP_SETTINGS'])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    return app

r = redis.Redis(host=os.environ['REDIS_LOCATION'], port=os.environ['REDIS_PORT'], db=0)
```

models.py
```python
from datetime import datetime
from config import db

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.String(128), unique=True)
    description = db.Column(db.String(128))
    price = db.Column(db.Float, default=0)

class Rule(db.Model):
    __tablename__ = 'rules'
    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(128))
    city = db.Column(db.String(128))
    sku = db.Column(db.String(128))
    min_condition = db.Column(db.Integer, default=0)
    max_condition = db.Column(db.Integer, default=0)
    variation = db.Column(db.Float, default=0)
```

### El archivo `requirements.txt`
Se puede utilizar el mismo contenido para el archivo requirements de ambos servicios:
```
alembic==1.0.11
Click==7.0
Flask==1.1.1
Flask-Migrate==2.5.2
Flask-SQLAlchemy==2.4.0
itsdangerous==1.1.0
Jinja2==2.10.1
Mako==1.1.0
MarkupSafe==1.1.1
psycopg2-binary==2.8.3
python-dateutil==2.8.0
python-editor==1.0.4
redis==3.2.1
requests
six==1.12.0
SQLAlchemy==1.3.6
Werkzeug==0.15.5
```

[Repositorio con el código fuente del proyecto(Nivel4)](https://github.com/darwinsalinas/nicaventas/tree/master/Nivel4/src)


