"""
Configuración centralizada del bot de Workana.

Este módulo contiene todas las constantes y configuraciones
necesarias para el funcionamiento del bot.
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Configuración del bot de Workana"""
    
    # Credenciales (desde archivo .env)
    WORKANA_EMAIL = os.getenv("WORKANA_EMAIL")
    WORKANA_PASS = os.getenv("WORKANA_PASS")
    # IA: Soporta "gemini" u "openai"
    AI_PROVIDER = os.getenv("AI_PROVIDER", "openai").lower()  # Por defecto OpenAI
    GEMINI_API_KEY = os.getenv("GEMINI_KEY")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
    # URLs de Workana
    BASE_URL = "https://www.workana.com"
    LOGIN_URL = "https://www.workana.com/login"
    SEARCH_URL = "https://www.workana.com/jobs?agreement=fixed&category=it-programming&language=xx&publication=1d&skills=angularjs%2Capi%2Cartificial-intelligence%2Cc-1%2Cc-2%2Ccss%2Cdjango%2Cdocker%2Cflask%2Chtml%2Cjava%2Cjavascript%2Claravel%2Cmysql%2Cnode-js%2Cphp%2Cpython%2Cqa-automation%2Creact-js%2Creact-native%2Creact-query%2Cresponsive-web-design%2Cselenium%2Csql%2Cweb-scraping"
    
    # Archivos de datos (en carpeta data/)
    DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    COOKIES_FILE = os.path.join(DATA_DIR, "workana_cookies.pkl")
    HISTORY_FILE = os.path.join(DATA_DIR, "history_proposals.json")
    
    # Límites y umbrales
    MAX_PROPOSALS_PER_DAY = 7  # Máximo de propuestas por día
    MAX_PROPOSALS_PER_WEEK = 52  # Máximo de propuestas por semana
    MAX_PROPOSALS_PER_EXECUTION = 6  # Propuestas por ejecución (para 52/semana con 2 ejecuciones/día)
    MIN_SCORE_TO_BID = 65  # Score mínimo para ofertar (0-100)
    PRICE_PERCENTAGE = 0.70  # Porcentaje del insight a usar (70%)
    MIN_BIDS_FOR_INSIGHT = 5  # Mínimo de propuestas para usar insight en lugar de IA
    
    # Configuración VPS
    HEADLESS_MODE = os.getenv("HEADLESS_MODE", "false").lower() == "true"  # Modo headless para VPS
    AUTO_MODE = os.getenv("AUTO_MODE", "false").lower() == "true"  # Modo automático (sin input de confirmación)
    SPEED_MODE = os.getenv("SPEED_MODE", "safe").lower()  # "fast" o "safe" (velocidad vs seguridad)
    
    # Delays configurables según modo
    if SPEED_MODE == "fast":
        # Modo rápido (más arriesgado pero 2-3x más rápido)
        DELAY_SCROLL = (0.1, 0.3)
        DELAY_TYPE = (0.02, 0.05)
        DELAY_CLICK = (0.2, 0.4)
        DELAY_PAGE = (1, 2)
        DELAY_BETWEEN_PROPOSALS = (120, 180)  # 2-3 minutos
    else:
        # Modo seguro (recomendado)
        DELAY_SCROLL = (0.2, 0.5)
        DELAY_TYPE = (0.03, 0.08)
        DELAY_CLICK = (0.3, 0.6)
        DELAY_PAGE = (2, 4)
        DELAY_BETWEEN_PROPOSALS = (180, 300)  # 3-5 minutos