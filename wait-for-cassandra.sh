#!/bin/bash
set -e

# Esperar a que Cassandra esté disponible
echo "Esperando a que Cassandra esté listo..."
until nc -z -v -w30 cassandra 9042; do
  echo "Cassandra no está listo aún. Reintentando en 5 segundos..."
  sleep 5
done

echo "Cassandra está listo. Iniciando consumidor de Spark..."

# Ejecutar el consumidor de Spark
exec "$@"

