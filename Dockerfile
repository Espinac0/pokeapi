# Usa una imagen base oficial de Python
FROM python:3.10-slim

# Establece un directorio de trabajo dentro del contenedor
WORKDIR /app

# Instalar Redis
RUN apt-get update && \
    apt-get install -y redis-server && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copia requirements.txt primero para aprovechar el caché de Docker
COPY requirements.txt .

# Instala las dependencias del proyecto
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto de los archivos del proyecto
COPY . .

# Variables de entorno para Redis
ENV REDIS_HOST=localhost \
    REDIS_PORT=6379

# Expone los puertos
EXPOSE 8000 6379

# Comando por defecto para iniciar la aplicación
CMD redis-server --daemonize yes && sleep 2 && python -m uvicorn main:app --host 0.0.0.0 --port 8000