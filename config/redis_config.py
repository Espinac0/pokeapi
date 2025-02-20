import redis

# Configuración del cliente Redis
redis_client = redis.Redis(
    host='localhost',  # Cambia esto si Redis está en otro host
    port=6379,        # Puerto por defecto de Redis
    db=0,             # Número de base de datos
    decode_responses=True  # Para que las respuestas sean strings en lugar de bytes
)
