#!/bin/sh
set -e

# Iniciar Redis en segundo plano
redis-server --daemonize yes

# Esperar un momento para asegurarse de que Redis esté listo
sleep 2

# Iniciar la aplicación
exec uvicorn main:app --host 0.0.0.0 --port 8000
