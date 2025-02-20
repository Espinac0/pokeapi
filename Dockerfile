# Usa una imagen base oficial de Python
FROM python:3.10-slim

# Establece un directorio de trabajo dentro del contenedor
WORKDIR /app

# Instalar Redis y configurar para que escuche en todas las interfaces
RUN apt-get update && \
    apt-get install -y redis-server && \
    sed -i 's/bind 127.0.0.1/bind 0.0.0.0/' /etc/redis/redis.conf && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copia requirements.txt primero para aprovechar el caché de Docker
COPY requirements.txt .

# Instala las dependencias del proyecto
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto de los archivos del proyecto
COPY . .

# Asegurar que start.sh tiene los permisos correctos y finales de línea Unix
RUN chmod +x start.sh && \
    sed -i 's/\r$//' start.sh

# Variables de entorno para Redis
ENV REDIS_HOST=localhost \
    REDIS_PORT=6379 \
    REDIS_DB=0

# Expone los puertos
EXPOSE 8000 6379

# Comando para ejecutar la aplicación
ENTRYPOINT ["/bin/sh", "start.sh"]