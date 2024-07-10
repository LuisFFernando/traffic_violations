# Registro de Infracciones de Transito

Registro de Infracciones de Transito es un servicio diseñado para Crear infracciones de transito a Conductores.

La administracion del servicio esta dada principalmente por el almacenamiento de los Agentes de Transito los cuales tienen la capacidad de crear usuarios(Conductores) y a estos relacionarles vehiculos, para posteriormente crear Infracciones relacionadas a estos.

Este Servicio cuenta con una seccion administrativa en Front con un crub basico para su funcionamiento.

![Descripción de la imagen](/diagrama_db.png)

Arquitectura Despliegue AWS

![Descripción de la imagen](/diagrama_despliegue.png)


-   Language: Python3
-   Framework: FastApi
-   Database: Postgres
-   Container: Docker

## Installation

1.  Para la instalacion en Local es necesario instalar poetry y ejecutar el siguiente comando

```
poetry install
```
-   Libraries:
    - fastapi
    - Postgresql
    - poetry
    - SqlAlembic

2. El environment se debe activar de forma automatica.

3. Para la ejecucion en local tenemos disponible el comando para validacion de linters

```
poetry run black .
```


## Documentation

- /api/v1/admin
- /api/v1/docs

## Status Services
- /api/v1/health


## **Execution**

**run Server**
```
$ docker-compose up -d
```

### Usage flow

1. Create customer POST `/api/v1/user`
2. Get User GET `/api/v1/user`


3. Crear migraciones para nuevos modelos
```
alembic revision --autogenerate -m "First migration-w"
```
4. Migrar Db
```
alembic upgrade head
```
export $(cat .env | xargs)


### Crear Infracciones

Para crear las infracciones debe existir un agente de transito creado desde el Admin, este usuario debera logearse
desde el siguiente endpoint y generar un Token para lograr el acceso a la creacion de Infracciones.

    - Login

    curl --location '{host}/api/v1/login' \
    --header 'accept: application/json' \
    --header 'Content-Type: application/json' \
    --data-raw '{
    "email": "manuel@mail.com",
    "password": "Manuel123"
    }'

Response

    {
    "success": true,
    "message": "OK",
    "data": {
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MjA1NjIxNDYsIm9mZmljZXJfaWQiOjF9.SsQcdHl7iKidEDpkrw-HR4iOBHNFrK-p5DLoV8pUz44"
    }
}


Despues de haber generado el login se debe enviar la peticion al siguiente endpoint definiendo el tipo de autenticacion como Bearer Token.

    curl --location '{host}/api/v1/cargar_infraccion' \
    --header 'Content-Type: application/json' \
    --header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MjA1NjIxNDYsIm9mZmljZXJfaWQiOjF9.SsQcdHl7iKidEDpkrw-HR4iOBHNFrK-p5DLoV8pUz44' \
    --data '{
        "placa_patente": "mnb-123",
        "timestamp": "2024-07-06 7:15:am",
        "comentarios": "Mal paqueado"
    }'

Response 

    {
        "success": true,
        "message": "OK",
        "data": {
            "comentarios": "Mal paqueado",
            "placa_patente": "mnb-123",
            "timestamp": "2024-07-06 7:15:am",
            "traffic_officer_id": 1,
            "active": true,
            "created_at": "2024-07-09 20:58:53.484971+00:00",
            "updated_at": "None"
        }
    }


Consultar Infracciones de un usuario

    curl --location '{host}/api/v1/generar_informe?email=muis%40mail.com' \
    --header 'accept: application/json'

Response 

    {
        "success": true,
        "message": "OK",
        "data": [
            {
                "id": 1,
                "brand": "Mazda",
                "model": "Mazda3 2023",
                "serial": "123123123",
                "description": "Color negro Sedan GT",
                "placa_patente": "mnb-123",
                "color": "Negro",
                "violations": [
                    {
                        "comentarios": "Mal paqueado",
                        "placa_patente": "mnb-123",
                        "timestamp": "2024-07-06 7:15:am",
                        "traffic_officer_id": 1,
                        "active": true,
                        "created_at": "2024-07-09 20:58:53.484971+00:00",
                        "updated_at": "None"
                    }
                ],
                "active": true,
                "created_at": "2024-07-09 20:57:31.933386+00:00",
                "updated_at": "None"
            }
        ]
    }