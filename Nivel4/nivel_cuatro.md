# Nivel 4

### Descripción general
La aplicación de NicaVentas cuenta con dos microservicios con una estructura bastante simple, los cuales fueron creados para interactuar con el servicio de base de datos(postgres) y el servicio de caché(redis), el primero de estos dos servicios es el servicio de consulta de disponilidad de ventas por pais y ciudades, el segundo es el servicio de consulta de condiciones de venta, en este segundo servicio se hace uso del API de OpenWeatherMaps para consultar el estado del clima en el pais y ciudad solicitado, esto con el fin de poder hacer una venta diferenciada de acuerdo al clima que se esté presentado en ese momento en la ciudad.

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

Servicio web se emplea para consultar si se está autorizada la venta de productos en general en una ciudad concreta de un país haciendo useo del endpoint `[GET] /active?city=leon&country=ni`.

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

Para calcular la respuesta adecuada, el endpoint `[POST] /quote` dispondrá del API de un tercero, concretamente de OpenWeather, para consultar el tiempo meteorológico de una ciudad concreta de un país. 

Con la información devuelta por el API de OpenWeather estamos en condiciones de comparar con las reglas de variación que hayamos creado en la base de datos:


| id_regla | ciudad | pais |     SKU | min_condition | max_condition | variation |
|---------:|-------:|-----:|--------:|--------------:|--------------:|----------:|
|        1 |   Leon |   NI | AZ00001 |           500 |           599 |       1.5 |
|        2 |   Leon |   NI | AZ00002 |           500 |           599 |       0.5 |
|          |        |      |         |               |               |           |

Supongamos que preguntamos al servicio meteorológico sobre las condiciones en Leon, Nicaragua, y obtenemos id=503 (very heavy rain). Consultamos a continuación a la base de datos y si se cumple al menos una regla de las que tengamos guardadas entonces el valor de `variation` será la variación que debemos usar. Si por el contrario no se cumpliera ninguna regla se podría considerar que la variación es 1, o lo que es lo mismo, que no hay variación.


## Procedimiento realizado para la creación y publicación de las imágenes de Docker
- URL de dockerhub del [servicio de consulta de disponibilidad](https://cloud.docker.com/repository/docker/darwinsalinas/nicaventas-disponibilidad-nivel4)

- URL de dockerhub del [servicio de consulta de condiciones de venta](https://cloud.docker.com/repository/docker/darwinsalinas/nicaventas-condiciones-nivel4)

Para crear una imagen de docker que pueda correr el código de nuestros Microservicios realizados con Flask se utilizó una imagen oficial de Docker para Python:

- URL de [imagen de Python](https://hub.docker.com/_/python)

Esta imagen contine lo necesario para correr código de python, por lo cual a partir de ella se ha creado la imagen que contiene el código del Microservicio, para reproducir una imagen igual a la que se ha creado debemos escribir el siguiente código en nuestro archivo Dockerfile:

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

Para construir las imagenes de docker y etiquetarlas ejecutamos esta línea en terminal dentro de la carpeta correspondiente de cada micro servicio:

```bash
docker build -t darwinsalinas/nicaventas-disponibilidad-nivel4 .
docker build -t darwinsalinas/nicaventas-condiciones-nivel4 .
```


Para subir nuestras imágenes recien creadas ejecutamos lo siguiente en terminal:

```bash
docker login && docker push darwinsalinas/nicaventas-condiciones-nivel4
docker login && docker push darwinsalinas/nicaventas-disponibilidad-nivel4
```
Al ejecutar las lineas de arriba se nos va a solicitar nuestras credenciales de dockerhub.


Para correr los servicios orquestados con docker-compose se require la presencia de un archivo de entorno `.env` que contenga todas las credenciales y configuraciones de la aplicacion:

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

Aparte del archivo de configuración anteriormente descrito, tambien necesitamos el script de `initdb.sql` para crear las tablas y rellenarla con datos para realizar pruebas:

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
INSERT INTO "public"."cities"("id", "city", "active", "country_id") VALUES (1, 'Leon', 't', 1);
INSERT INTO "public"."cities"("id", "city", "active", "country_id") VALUES (2, 'Chinandega', 't', 1);
INSERT INTO "public"."cities"("id", "city", "active", "country_id") VALUES (3, 'Matagalpa', 't', 1);
INSERT INTO "public"."cities"("id", "city", "active", "country_id") VALUES (4, 'Managua', 't', 1);
INSERT INTO "public"."cities"("id", "city", "active", "country_id") VALUES (5, 'Granada', 't', 1);

INSERT INTO "public"."products"("id", "sku", "description", "price") VALUES (1, 'AZ00001', 'Paraguas de señora estampado', 10);
INSERT INTO "public"."products"("id", "sku", "description", "price") VALUES (2, 'AZ00002', 'Helado de sabor fresa', 1);

INSERT INTO "public"."rules"("id", "country", "city", "sku", "min_condition", "max_condition", "variation") VALUES (1, 'ni', 'Leon', 'AZ00001', 500, 599, 1.5);
INSERT INTO "public"."rules"("id", "country", "city", "sku", "min_condition", "max_condition", "variation") VALUES (2, 'ni', 'Leon', 'AZ00002', 500, 599, 0.5);
INSERT INTO "public"."rules"("id", "country", "city", "sku", "min_condition", "max_condition", "variation") VALUES (3, 'ni', 'Leon', 'AZ00002', 800, 810, 1.5);
INSERT INTO "public"."rules"("id", "country", "city", "sku", "min_condition", "max_condition", "variation") VALUES (4, 'ni', 'Leon', 'AZ00001', 800, 810, 0.5);
INSERT INTO "public"."rules"("id", "country", "city", "sku", "min_condition", "max_condition", "variation") VALUES (5, 'ni', 'Managua', 'AZ00001', 500, 599, 1.5);
INSERT INTO "public"."rules"("id", "country", "city", "sku", "min_condition", "max_condition", "variation") VALUES (6, 'ni', 'Managua', 'AZ00002', 500, 599, 0.5);
INSERT INTO "public"."rules"("id", "country", "city", "sku", "min_condition", "max_condition", "variation") VALUES (7, 'ni', 'Managua', 'AZ00002', 800, 810, 1.5);
INSERT INTO "public"."rules"("id", "country", "city", "sku", "min_condition", "max_condition", "variation") VALUES (8, 'ni', 'Managua', 'AZ00001', 800, 810, 0.5);
INSERT INTO "public"."rules"("id", "country", "city", "sku", "min_condition", "max_condition", "variation") VALUES (9, 'ni', 'Chinandega', 'AZ00001', 500, 599, 1.5);
INSERT INTO "public"."rules"("id", "country", "city", "sku", "min_condition", "max_condition", "variation") VALUES (10, 'ni', 'Chinandega', 'AZ00002', 500, 599, 0.5);
INSERT INTO "public"."rules"("id", "country", "city", "sku", "min_condition", "max_condition", "variation") VALUES (11, 'ni', 'Chinandega', 'AZ00002', 800, 810, 1.5);
INSERT INTO "public"."rules"("id", "country", "city", "sku", "min_condition", "max_condition", "variation") VALUES (12, 'ni', 'Chinandega', 'AZ00001', 800, 810, 0.5);
INSERT INTO "public"."rules"("id", "country", "city", "sku", "min_condition", "max_condition", "variation") VALUES (13, 'ni', 'Bluefields', 'AZ00001', 500, 599, 1.5);
INSERT INTO "public"."rules"("id", "country", "city", "sku", "min_condition", "max_condition", "variation") VALUES (14, 'ni', 'Bluefields', 'AZ00002', 500, 599, 0.5);
INSERT INTO "public"."rules"("id", "country", "city", "sku", "min_condition", "max_condition", "variation") VALUES (15, 'ni', 'Bluefields', 'AZ00002', 800, 810, 1.5);
INSERT INTO "public"."rules"("id", "country", "city", "sku", "min_condition", "max_condition", "variation") VALUES (16, 'ni', 'Bluefields', 'AZ00001', 800, 810, 0.5);
INSERT INTO "public"."rules"("id", "country", "city", "sku", "min_condition", "max_condition", "variation") VALUES (17, 'ni', 'Nueva Guinea', 'AZ00001', 500, 599, 1.5);
INSERT INTO "public"."rules"("id", "country", "city", "sku", "min_condition", "max_condition", "variation") VALUES (18, 'ni', 'Nueva Guinea', 'AZ00002', 500, 599, 0.5);
INSERT INTO "public"."rules"("id", "country", "city", "sku", "min_condition", "max_condition", "variation") VALUES (19, 'ni', 'Nueva Guinea', 'AZ00002', 800, 810, 1.5);
INSERT INTO "public"."rules"("id", "country", "city", "sku", "min_condition", "max_condition", "variation") VALUES (20, 'ni', 'Nueva Guinea', 'AZ00001', 800, 810, 0.5);
INSERT INTO "public"."rules"("id", "country", "city", "sku", "min_condition", "max_condition", "variation") VALUES (21, 'ni', 'Juigalpa', 'AZ00001', 500, 599, 1.5);
INSERT INTO "public"."rules"("id", "country", "city", "sku", "min_condition", "max_condition", "variation") VALUES (22, 'ni', 'Juigalpa', 'AZ00002', 500, 599, 0.5);
INSERT INTO "public"."rules"("id", "country", "city", "sku", "min_condition", "max_condition", "variation") VALUES (23, 'ni', 'Juigalpa', 'AZ00002', 800, 810, 1.5);
INSERT INTO "public"."rules"("id", "country", "city", "sku", "min_condition", "max_condition", "variation") VALUES (24, 'ni', 'Juigalpa', 'AZ00001', 800, 810, 0.5);
INSERT INTO "public"."rules"("id", "country", "city", "sku", "min_condition", "max_condition", "variation") VALUES (25, 'ni', 'Rivas', 'AZ00001', 500, 599, 1.5);
INSERT INTO "public"."rules"("id", "country", "city", "sku", "min_condition", "max_condition", "variation") VALUES (26, 'ni', 'Rivas', 'AZ00002', 500, 599, 0.5);
INSERT INTO "public"."rules"("id", "country", "city", "sku", "min_condition", "max_condition", "variation") VALUES (27, 'ni', 'Rivas', 'AZ00002', 800, 810, 1.5);
INSERT INTO "public"."rules"("id", "country", "city", "sku", "min_condition", "max_condition", "variation") VALUES (28, 'ni', 'Rivas', 'AZ00001', 800, 810, 0.5);
```

Ya con estos archivos podemos correr nuestros servicios con la siguiente instrucción:

```bash
docker-compose up
```

Si queremos poner a correr ls servicios en segundo plano podemos agregarle el flag `-d`:
```bash
docker-compose up -d
```

Si pusiste los servicios en segundo plano puedes ver lo que ocurre dentro de los contendores con el comando:

```bash
docker logs -f nicaventas-db
```



## Probar el funcionamiento de los microservicios


Probar con `curl localhost:8000/active?city=leon&country=ni`. La respuesta debe ser una respuesta JSON válida conforme a la especificación del servicio.



# Nivel 2

Crear las tablas y los datos semilla en la base de datos
docker-compose run nicaventas-us python seed_database.py

Detener los serivicios orquetados con docker-compose
docker-compose down



# Nivel 4

http://api.openweathermap.org/data/2.5/weather?q=London,uk&APPID=3d3ea700fcb655178274e26b3af34ccd&units=metric


https://redis-py.readthedocs.io/en/latest/


https://flask.palletsprojects.com/en/1.1.x/patterns/errorpages/