Este documento proporciona los pasos para construir, configurar y ejecutar los servicios del sistema de monitoreo de tráfico en tiempo real. Incluye instrucciones para configurar la base de datos Cassandra y ejecutar los scripts necesarios.

Requisitos Previos
Docker y Docker Compose instalados.
Python 3 instalado en el contenedor del scrapper.
Imagen de Cassandra configurada en Docker.
Construcción e Inicio de los Servicios
Construir e iniciar los servicios
Ejecute el siguiente comando para construir e iniciar los servicios definidos en el archivo
NUEVO
[22:09]
docker-compose up --build
NUEVO
[22:09]
Verificar los logs del servicio consumidor de Spark
Para comprobar que el servicio consumidor de Spark está ejecutándose correctamente, use:
[22:09]
docker logs consumer-spark
[22:09]
Ejecución del Scrapper
Acceder al contenedor del scrapper
Ingrese al contenedor del scrapper con:
NUEVO
[22:09]
docker exec -it scrapper bash
NUEVO
[22:09]
python3 scrapper.py
[22:09]
Configuración de Cassandra
Acceder al contenedor de Cassandra
Use el siguiente comando para entrar en el contenedor de Cassandra:
NUEVO
[22:10]
docker exec -it cassandra cqlsh
NUEVO
[22:10]
Crear el Keyspace
Cree un Keyspace para almacenar los datos de monitoreo de tráfico:
[22:10]
CREATE KEYSPACE IF NOT EXISTS traffic_monitoring
WITH replication = {'class': 'SimpleStrategy', 'replication_factor' : 1};
NUEVO
[22:10]
Usar el Keyspace
Seleccione el Keyspace creado:
[22:10]
USE traffic_monitoring;
[22:10]
Crear la tabla para alertas
Cree la tabla alerts con la estructura adecuada:CREATE TABLE IF NOT EXISTS alerts (
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
); (editado)
NUEVO
NUEVO
[22:10]
Consultar los datos almacenados
Verifique los datos en la tabla con:
NUEVO
[22:11]
SELECT * FROM alerts;
