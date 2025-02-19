import redis
import os

# Configuración de Redis usando variables de entorno
redis_host = os.getenv('REDIS_HOST', 'redis')  # Cambiado a 'redis' como nombre del servicio
redis_port = int(os.getenv('REDIS_PORT', 6379))

# Configuración de Redis
redis_client = redis.Redis(host=redis_host, port=redis_port, db=0, decode_responses=True)

def is_redis_working():
    try:
        redis_client.ping()
        return True
    except redis.ConnectionError:
        return False
