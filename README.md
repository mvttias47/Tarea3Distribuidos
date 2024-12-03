Sistema de Monitoreo de Tráfico en Tiempo Real
Este proyecto implementa un sistema distribuido para monitorear el tráfico en tiempo real, inspirado en aplicaciones como Waze. Utiliza tecnologías distribuidas como scrapping, Apache Kafka, Apache Spark, Apache Cassandra y Elasticsearch para extraer, procesar, almacenar y consultar datos relacionados con alertas de tráfico.

Configuración y Ejecución
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


