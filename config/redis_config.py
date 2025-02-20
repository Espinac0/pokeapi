import redis
import os

# Configuración del cliente Redis usando variables de entorno
redis_client = redis.Redis(
    host=os.getenv('REDIS_HOST', 'localhost'),
    port=int(os.getenv('REDIS_PORT', 6379)),
    db=int(os.getenv('REDIS_DB', 0)),
    decode_responses=True
)

# Función para verificar la conexión a Redis
def check_redis_connection():
    try:
        redis_client.ping()
        return True
    except redis.ConnectionError:
        return False
