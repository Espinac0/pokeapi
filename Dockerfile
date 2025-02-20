# Usa una imagen base oficial de Python
FROM python:3.10-slim

# Establece un directorio de trabajo dentro del contenedor
WORKDIR /app

# Instalar Redis y configurar para que escuche en todas las interfaces
RUN apt-get update && \
    apt-get install -y redis-server && \
    sed -i 's/bind 127.0.0.1/bind 0.0.0.0/' /etc/redis/redis.conf

# Copia requirements.txt primero para aprovechar el caché de Docker
COPY requirements.txt .

# Instala las dependencias del proyecto
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto de los archivos del proyecto
COPY . .

# Script para iniciar Redis y la aplicación
COPY start.sh .
RUN chmod +x start.sh

# Variables de entorno para Redis
ENV REDIS_HOST=localhost
ENV REDIS_PORT=6379
ENV REDIS_DB=0

# Expone los puertos
EXPOSE 8000 6379

# Comando para ejecutar la aplicación
CMD ["./start.sh"]