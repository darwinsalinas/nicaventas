# Nivel 1

### Objetivos:
 - Desarrollar un microservicio en `flask` que implemente la llamada `[GET] /active` con una respuesta _dummy_ fija
 - Crear una imagen docker que contenga dicho microservicio y publicarla en `dockerhub`

#### Procedimiento realizado para la creaion del API/Microservicio
Para completar esta parte se desarrolló el API(microservicio) que responde una respuesta fija, en este caso el API está preparado para recibir dos parámetros(country y city) por medio de la URL en el endpoint `/active`

La estructura de carpetas y archivos para nuestra aplicación Flask es la siguiente:

```bash
└── src
    ├── Dockerfile
    └── disponibilidad
        ├── app.py
        └── requirements.txt
```


En la ruta principal de la aplicación se responde con un json de bienvenida/saludo, en el cual se brindan algunos datos de la aplicación:

```json
{
    "id": "nica-ventas",
    "version": "0.1",
    "status": "development"
}
```

Para poder enviar la respuesta anterior se utilizó el siguiente código:
```python
@app.route('/')
def info():
    info = {
        'id': 'nica-ventas',
        'version': '0.1',
        'status': 'development'
    }
    return jsonify(info)
```

En el endpoint `/active` la aplicación responde con un json de acuerdo a la  especificación del servicio:

```json
{
    "active": false,
    "city": "leon",
    "country": "ni"
}

```
En este caso el endpoint `/active` está preparado para recibir dos parámetros de tipo GET(por medio de la URL) pero la respuesta NO proviene de la base de datos, sino que solamente muestra con cierto formato los datos que han sido enviados como parámetros, esto es porque en la aplicación flask se reciben los argumentos de esta manera:

```python
@app.route('/active') #/active?city=leon&country=ni
def city_is_active():
    country = request.args.get("country", "ni")
    city = request.args.get("city", "Managua")
    info = {
        "active": False,
        "country": country,
        "city": city
    }
    return jsonify(info)

```
Como se puede apreciar en el fragmento de código anterior simplemente se reciben los parametros por URL utilizando `request` para recibirlos y almacenarlos en variables que posteriormente son asignadas a las claves de un diccionario de python y finalmente son devueltos en formato json, para lo cual se utiliza `jsonify` y el diccionario creado previamente llamado `info`



#### Procedimiento realizado para la creación y publciación de la imagen de Docker
- URL de dockerhub [(https://hub.docker.com/r/darwinsalinas/nicaventasnivel1)](https://hub.docker.com/r/darwinsalinas/nicaventasnivel1)


Para crear una imagen de docker que pueda correr el código de nuestro Microservicio realizado con Flask se utilizó una imagen oficial de Docker para Python:

- URL de imagen de Python [(https://hub.docker.com/_/python)](https://hub.docker.com/_/python)

Esta imagen contine lo necesario para correr código de python, por lo cual a partir de ella se ha creado la imagen que contiene el código del Microservicio, para reproducir una imagen igual a la que se ha creado debemos escribir el siguiente código en nuestro archivo Dockerfile:

```
FROM python
LABEL maintainer "Darwin Salinas <salinash2000@gmail.com>"
RUN apt-get update
RUN mkdir /app
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r disponibilidad/requirements.txt
CMD ["python", "disponibilidad/app.py"]
```

Puedes reemplazar el nombre y correo del `manteiner` de la imagen

Para construir y etiquetar la imagen ejecutamos esta línea en terminal:

```bash
docker build -t darwinsalinas/nicaventasnivel1 .
```


Para subir nuestra imagen recien creada ejecutamos la siguiente linea en terminal:

```bash
docker login && docker push darwinsalinas/nicaventasnivel1
```
Esto nos va a solicitar nuestras credenciales de dockerhub

Para correr un contenedor basado en nuestra imagen podemos ejecutar esta linea en terminal:

```bash
docker run -d -p 8000:8000 darwinsalinas/nicaventasnivel1:latest
```

Con el flag `-d` ponemos nuestro contenedor en background
Con el flag `-p 8000:8000` especificamos el mapeo de los puertos hacia nuestro contenedor y en el cual vamos a correr nuestra aplicación



Probar con `curl localhost:8000/active?city=leon&country=ni`. La respuesta debe ser una respuesta JSON válida conforme a la especificación del servicio.



# Nivel 2


Construir la imagen que contiene el micro servicio
```bash
docker build -t darwinsalinas/nicaventasnivel2 .
```

Se requiere docker-compose
Se requiere .env con las credenciales para la base de datos

docker build

export DATABASE_URL="postgresql://localhost/nicaventas"
export APP_SETTINGS="config.DevelopmentConfig"


Arrancar los contenedores orquestados con docker-compose:
docker-compose up -d

Ver los logs del contenedor de la base de datos:
docker logs -f postgres_nicaventas

Crear la base de datos nicaventas
docker exec -it postgres_nicaventas psql -U postgres -c "create database nicaventas"

Crear las tablas y los datos semilla en la base de datos
docker-compose run nicaventas-us python seed_database.py

Detener los serivicios orquetados con docker-compose
docker-compose down

https://github.com/realpython/orchestrating-docker

https://realpython.com/dockerizing-flask-with-compose-and-machine-from-localhost-to-the-cloud/


https://www.saltycrane.com/blog/2019/01/how-run-postgresql-docker-mac-local-development/


https://github.com/realpython/orchestrating-docker




# Nivel 4
construir la imagen para el servicios de condiciones

docker build -t darwinsalinas/nicaventascondicionesnivel4 .


http://api.openweathermap.org/data/2.5/weather?q=London,uk&APPID=3d3ea700fcb655178274e26b3af34ccd&units=metric


https://redis-py.readthedocs.io/en/latest/


https://flask.palletsprojects.com/en/1.1.x/patterns/errorpages/