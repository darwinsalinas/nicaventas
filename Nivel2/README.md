# Nicaventas Nivel 2
Esta aplicación fue creada con `python`, `postgres` y el micro framewok `Flask`, (entre otras librerias/dependencias) se ha creado una imagen de docker basada en la [imagen oficial de Python](https://hub.docker.com/_/python). 

La estructura directorios y archivos de la aplicación es la siguiente:
```bash
src
├── disponibilidad
│   ├── .env
│   ├── Dockerfile
│   ├── app.py
│   ├── config.py
│   ├── models.py
│   ├── requirements.txt
│   └── seed_database.py
├── docker-compose.yml
```

## El archivo Dockerfile
Para crear la imagen con el micro servicio se ha creado un archivo Dockerfile con el siguiente contenido:

```Docker
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
A continuacion un explicación corta de lo que hace el archivo Dockerfile:

En el archivo Dockerfile se especifica de que imagen de Docker vamos a heredar o extender:

```
FROM python
```

Crear una carpeta dentro y poner los archivos de la aplicación Flask dentro del la imagen:
```
RUN mkdir /app
WORKDIR /app
COPY . /app
```

Instalar los requerimientos especificados en el archivo de requirements.txt:
```
RUN pip install -r requirements.txt
```

Tambien en esta imagen se ha agregado un script que permite ejecutar la aplicación hasta que alguno de los serivios de los cuales depende se encuentre disponible

```
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.2.1/wait /wait
RUN chmod +x /wait
```

Ya por ultimo se ejecuta el comando que arranca la aplicación:
```
CMD /wait && python app.py
```

### Construir la imagen

Para construir la imagen se debe ejecutar el siguiente comando en la terminal, en la misma ruta donde se encuentra ubicado el archivo Dockerfile:
```bash
docker build -t darwinsalinas/nicaventas-disponibilidad-nivel2 .
```
En mi caso yo le he construido y etiquetado para poderla subir a [mi repositorio de docker hub](https://cloud.docker.com/u/darwinsalinas/repository/list) posteriormente, para saubir la imagen de recien construida se debe ejecutar el siguiente comando en la terminal:
```bash
docker login && docker push darwinsalinas/nicaventas-disponibilidad-nivel2
```


## La receta con docker-compose
Para probar de forma fácil el funcionamiento del microservicio creado se ha creado una receta con docker-compose, el cual orquesta un servicio para la base de datos y el servicio para la aplicacion Flask.

```docker
version: '3'
services:
  nicaventas-db:
    image: postgres
    restart: always
    container_name: "nicaventas-db"
    env_file:
      - .env
    ports:
      - "54320:5432"
    # Activar este volume si se quieren rellenar la base de datos
    # volumes:
    #   - ./initdb.sql:/docker-entrypoint-initdb.d/initdb.sql

  nicaventas-us:
    restart: always
    depends_on:
      - nicaventas-db
    environment:
      WAIT_HOSTS: nicaventas-db:5432
    container_name: "nicaventas-us"
    image: darwinsalinas/nicaventas-disponibilidad-nivel2
    env_file:
      - .env
    ports:
      - 5000:5000
    command: flask run --host=0.0.0.0
```

Como se puede apreciar en el archivo `docker-compose` se especifican los servicios que se deben arrancar y para el correcto funcinamiento de los mismos  primeramente necesitamos crear un archivo `.env` con las configuraciones y credenciales de nuestra bade de datos:

```bash
POSTGRES_DB=nicaventas
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_PORT=5432
DB_SERVICE=nicaventas-db
APP_SETTINGS=config.DevelopmentConfig
FLASK_DEBUG=1
TOKEN=2234hj234h2kkjjh42kjj2b20asd6918
```
Este archivo de entorno (.env) será compartido con ambos servicios, en él tendremos el nombre de la base de datos a la cual debe conectarse nuestra aplicación Flask, en este caso la base de datos llamada `nicaventas`.

Ademas del nombre de la base de datos tambien tenemos algunas configuraciones para el entorno de Flask, especificamente el modo de depuración está activado en esta configuracón.


### Arrancar los contenedores orquestados con docker-compose:
```bash
docker-compose up -d
```

Como hemos arrancado la aplicacion y la base de datos en backgroud podemos ver los logs de lo que está ocurriendo en nuestros contendores con el siguiente comando:

```bash
docker logs -f nicaventas-db
```
En este caso especificamente veremos los logs del servicio de la base de datos.

Si por algun motivo la base datos no se crea automáticamente tambien podemos crear la base de datos de forma manual con la siguiente instrucción en la terminal:

```bash
docker exec -it nicaventas-db psql -U postgres -c "create database nicaventas"
```

De igual manera se dispone de un script que permite poblar la base de datos con algunos datos para hacer pruebas, esto puede hacerse con la siguiente instrucción en la terminal:

```bash
docker-compose run nicaventas-us python seed_database.py
```

Para detener los serivicios orquetados con docker-compose se debe ejecutar el siguiente comando en la tarminal:
```bash
docker-compose down
```

## Funcionamiento del servicio de consulta de disponibilidad de ventas

Servicio web se emplea para consultar si se está autorizada la venta de productos en general en una ciudad concreta de un país. Para ello se contruirá un API REST, y concretamente para esta consulta se implementará un endpoint `[GET] /active?city=leon&country=ni`.

El resultado de la invocación de este endpoint, a modo de ejemplo, será el siguiente:

```json
{
  "active": true,
  "country": "ni",
  "city": "Leon"
}
```


El campo `active` indica si la venta está autorizada (`true`) o no (`false`) en la correspondiente ciudad (`city`) del país (`country`) especificado en la llamada.

Una serie de operadores son los encargados de activar y desactivar las posibilidades de venta en las ciudades. Estos operadores el siguiente endpoint del API para activar o desactivar la venta:


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

El token es un secreto compartido entre los encargados y el sistema. Para este ejemplo, el token `2234hj234h2kkjjh42kjj2b20asd6918` será siempre este.










