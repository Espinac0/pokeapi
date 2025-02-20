# Usa una imagen base oficial de Python
FROM python:3.10-slim

# Establece un directorio de trabajo dentro del contenedor
WORKDIR /app

# Instalar Redis
RUN apt-get update && apt-get install -y redis-server

# Copia requirements.txt primero para aprovechar el caché de Docker
COPY requirements.txt .

# Instala las dependencias del proyecto
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto de los archivos del proyecto
COPY . .

# Script para iniciar Redis y la aplicación
COPY start.sh .
RUN chmod +x start.sh

# Expone el puerto donde correrá la aplicación
EXPOSE 8000 6379

# Comando para ejecutar la aplicación
CMD ["./start.sh"]