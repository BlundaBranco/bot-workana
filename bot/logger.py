"""
Configuración centralizada de logs.

Permite ver la actividad del bot tanto en consola como en archivo,
con rotación automática para evitar archivos gigantes.
"""

import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logger(name="WorkanaBot"):
    """
    Configura y devuelve un logger robusto.
    
    Guarda logs en: logs/bot_execution.log
    Nivel: INFO
    Formato: [FECHA HORA] [NIVEL] Mensaje
    """
    # Crear carpeta de logs si no existe
    log_dir = os.path.join(os.getcwd(), "logs")
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "bot_execution.log")

    # Crear logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Evitar duplicar handlers si ya existen
    if logger.handlers:
        return logger

    # Formatter
    formatter = logging.Formatter(
        '[%(asctime)s] [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # 1. Handler para Archivo (con rotación 5MB, backup=2)
    file_handler = RotatingFileHandler(
        log_file, 
        maxBytes=5*1024*1024,  # 5 MB
        backupCount=2,
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    # 2. Handler para Consola (para ver mientras testeas)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)

    # Añadir handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

# Instancia global para importar fácilmente
logger = setup_logger()
