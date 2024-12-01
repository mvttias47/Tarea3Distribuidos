from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, explode
from pyspark.sql.types import StructType, StructField, StringType, TimestampType
from elasticsearch import Elasticsearch
from cassandra.cluster import Cluster
import json

# Crear la sesión de Spark con configuración específica
spark = SparkSession.builder \
    .appName("WazeIncidentProcessor") \
    .config("spark.es.nodes", "localhost") \
    .config("spark.es.port", "9200") \
    .config("spark.es.nodes.wan.only", "true") \
    .config("spark.cassandra.connection.host", "localhost") \
    .getOrCreate()

# Configurar el nivel de log para ver más información
spark.sparkContext.setLogLevel("INFO")
print("Sesión Spark creada exitosamente")

# Definir el schema basado en la estructura JSON que mostraste
schema = StructType([
    StructField("type", StringType(), True),
    StructField("position", StringType(), True),
    StructField("timestamp", StringType(), True)
])

print("Intentando conectar con Kafka...")

# Leer datos de Kafka con más opciones de configuración
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9093") \
    .option("subscribe", "waze-incidents") \
    .option("startingOffsets", "earliest") \
    .option("failOnDataLoss", "false") \
    .load()

print("Conexión con Kafka establecida")

# Convertir el valor de Kafka (que está en formato binario) a string
value_df = df.selectExpr("CAST(value AS STRING)")

# Parsear el JSON
parsed_df = value_df.select(
    from_json(col("value"), schema).alias("data")
).select("data.*")

print("Esquema del DataFrame:")
parsed_df.printSchema()

# Función para procesar cada batch
def process_batch(df, epoch_id):
    print(f"Procesando batch {epoch_id}")
    print(f"Número de registros en este batch: {df.count()}")
    
    # Mostrar algunos registros de ejemplo
    df.show(truncate=False)
    
    # Escribir a Elasticsearch
    try:
        df.write \
            .format("org.elasticsearch.spark.sql") \
            .option("es.nodes", "localhost") \
            .option("es.port", "9200") \
            .option("es.resource", "waze-incidents") \
            .option("es.mapping.id", "timestamp") \
            .mode("append") \
            .save()
        print(f"Batch {epoch_id} escrito en Elasticsearch exitosamente")
    except Exception as e:
        print(f"Error escribiendo en Elasticsearch: {str(e)}")
    
    # Escribir a Cassandra
    try:
        df.write \
            .format("org.apache.spark.sql.cassandra") \
            .option("spark.cassandra.connection.host", "localhost") \
            .option("keyspace", "your_keyspace") \
            .option("table", "waze_incidents") \
            .mode("append") \
            .save()
        print(f"Batch {epoch_id} escrito en Cassandra exitosamente")
    except Exception as e:
        print(f"Error escribiendo en Cassandra: {str(e)}")

# Iniciar el streaming con procesamiento por batch
query = parsed_df.writeStream \
    .foreachBatch(process_batch) \
    .outputMode("append") \
    .start()

print("Streaming iniciado")

# Esperar a que termine el streaming
try:
    query.awaitTermination()
except KeyboardInterrupt:
    print("Deteniendo el streaming...")
    query.stop()
    print("Streaming detenido")
except Exception as e:
    print(f"Error en el streaming: {str(e)}")
finally:
    spark.stop()
