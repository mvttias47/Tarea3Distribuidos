Sistema de Monitoreo de Tráfico en Tiempo Real
Este proyecto implementa un sistema distribuido para monitorear el tráfico en tiempo real, inspirado en aplicaciones como Waze. Utiliza tecnologías distribuidas como scrapping, Apache Kafka, Apache Spark, Apache Cassandra y Elasticsearch para extraer, procesar, almacenar y consultar datos relacionados con alertas de tráfico.

Configuración y Ejecución
NUEVO
[23:55]
Construir e iniciar los servicios:

bash
Copy code
docker-compose up --build
Verificar los logs del servicio consumidor de Spark:

bash
Copy code
docker logs consumer-spark
Acceder al contenedor del scrapper y ejecutar el script de scrapping:

bash
Copy code
docker exec -it scrapper bash
python3 scrapper.py
Configurar la base de datos Cassandra:
NUEVO
[23:56]
Acceder al contenedor de Cassandra:

bash
Copy code
docker exec -it cassandra cqlsh
Crear el Keyspace:

sql
Copy code
CREATE KEYSPACE IF NOT EXISTS traffic_monitoring
WITH replication = {'class': 'SimpleStrategy', 'replication_factor' : 1};
Usar el Keyspace:

sql
Copy code
USE traffic_monitoring;
Crear la tabla para almacenar las alertas:

sql
Copy code
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
Consultar los datos almacenados:

sql
Copy code
SELECT * FROM alerts

