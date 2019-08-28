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

