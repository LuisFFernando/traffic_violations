# Registro de Infracciones de Transito

Registro de Infracciones de Transito es un servicio diseñado para Crear infracciones de transito a Conductores.

La administracion del servicio esta dada principalmente por el almacenamiento de los Agentes de Transito los cuales tienen la capacidad de crear usuarios(Conductores) y a estos relacionarles vehiculos, para posteriormente crear Infracciones relacionadas a estos.

Este Servicio cuenta con una seccion administrativa en Front con un crub basico para su funcionamiento

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



