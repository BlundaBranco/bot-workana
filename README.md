# 🤖 Bot de Workana - Guía Rápida

## 📁 Estructura del Proyecto

```
bot_workana/
├── bot/                    # Código principal
│   ├── __init__.py        # Exporta clases principales
│   ├── config.py          # Configuración (límites, URLs, delays)
│   ├── ai_assistant.py    # Análisis de proyectos con IA
│   └── workana_bot.py     # Lógica del bot (scraping, envío)
│
├── data/                   # Datos persistentes
│   ├── workana_cookies.pkl      # Cookies de sesión
│   └── history_proposals.json   # Historial de propuestas
│
├── docs/                   # Documentación
│   ├── ARCHIVOS.md        # Descripción de cada archivo
│   └── ESTRATEGIA.md       # Análisis de estrategia
│
├── main.py                 # Ejecución manual (una vez)
├── scheduler.py            # Ejecución programada (VPS)
├── test_auto.py            # Pruebas locales (modo auto)
├── setup_vps.sh           # Script de instalación VPS
├── requirements.txt        # Dependencias Python
├── GUIA_VPS.md            # ⭐ Guía paso a paso para DigitalOcean
└── .env                    # Credenciales (crear manualmente)
```

## 🚀 Setup Rápido

### 1. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 2. Crear archivo `.env`
```env
WORKANA_EMAIL=tu_email@ejemplo.com
WORKANA_PASS=tu_password
GEMINI_KEY=tu_api_key_gemini
HEADLESS_MODE=false
AUTO_MODE=false
SPEED_MODE=safe
```

### 3. Ejecutar
```bash
# Prueba local (con navegador visible)
python main.py

# Prueba automática (sin inputs)
python test_auto.py
```

## 📊 Configuración: 52 Propuestas/Semana

**Horarios optimizados:**
- **2 ejecuciones diarias**: 09:00 y 17:00
- **Días**: Lunes a Viernes
- **Propuestas por ejecución**: 5-6
- **Total semanal**: ~50-52 propuestas

Ver `scheduler.py` para ajustar horarios.
