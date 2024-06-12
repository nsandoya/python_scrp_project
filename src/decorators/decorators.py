import time
import logging # Para registrar mensajes

# Configurar el registro de logs
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Configuración del registro de mensajes
# Marca de tiempo, nivel de mensaje y mensaje
def timethis(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        total_time = end_time - start_time
        logging.info(f"{func.__name__} executed in {total_time:.4f} seconds")
        return result
    return wrapper


def logthis(func):
    def wrapper(*args, **kwargs):
        logging.info(f"Running {func.__name__}")  # Se registra el inicio de la ejecución de la función
        result = func(*args, **kwargs)  # Se ejecuta la función original
        logging.info(f"Done {func.__name__}")  # Se registra el fin de la ejecución de la función original
        return result  # Retornamos el resultado de la función original
    return wrapper