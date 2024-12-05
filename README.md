# Sistema de Monitoreo de Tráfico en Tiempo Real

Este documento proporciona los pasos para construir, configurar y ejecutar los servicios del sistema de monitoreo de tráfico en tiempo real. Incluye instrucciones para configurar la base de datos Cassandra y ejecutar los scripts necesarios.

## Requisitos Previos

Docker y Docker Compose instalados. Python 3 instalado en el contenedor del scrapper. Imagen de Cassandra configurada en Docker.

## Construcción e Inicio de los Servicios

Construir e iniciar los servicios: Ejecute el siguiente comando para construir e iniciar los servicios definidos en el archivo:

`docker-compose up --build`

Verificar los logs del servicio consumidor de Spark: Para comprobar que el servicio consumidor de Spark está ejecutándose correctamente, use:

`docker logs consumer-spark`

## Ejecución del Scrapper

Acceder al contenedor del scrapper: Ingrese al contenedor del scrapper con:

`docker exec -it scrapper bash`

Luego, ejecute el script dentro del contenedor:

`python3 scrapper.py`

## Configuración de Cassandra

Acceder al contenedor de Cassandra: Use el siguiente comando para entrar en el contenedor de Cassandra:

`docker exec -it cassandra cqlsh`

Crear el Keyspace: Cree un Keyspace para almacenar los datos de monitoreo de tráfico con el siguiente comando:

`CREATE KEYSPACE IF NOT EXISTS traffic_monitoring WITH replication = {'class': 'SimpleStrategy', 'replication_factor' : 1};`

Usar el Keyspace: Seleccione el Keyspace creado con el siguiente comando:

`USE traffic_monitoring;`

Crear la tabla para alertas: Cree la tabla `alerts` con la estructura adecuada:

```sql
CREATE TABLE IF NOT EXISTS alerts (
    uuid text PRIMARY KEY,
    country text,
    city text,
    reliability int,
    type text,
    speed int,
    subtype text,
    street text,
    id text,
    ncomments int,
    inscale boolean,
    confidence int,
    roadtype int,
    location_x double,
    location_y double,
    pubmillis bigint
);

