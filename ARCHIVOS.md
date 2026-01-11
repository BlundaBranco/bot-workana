# 📁 Descripción de Archivos

## 🎯 Archivos Principales (NO TOCAR)

### `main.py`
**Qué hace**: Ejecuta el bot una sola vez (para pruebas manuales)
**Cuándo usar**: Pruebas locales, debugging
**No usar en**: VPS (usa `scheduler.py`)

### `scheduler.py`
**Qué hace**: Ejecuta el bot automáticamente en horarios programados
**Cuándo usar**: En VPS, producción
**Configuración**: Horarios en `HORARIOS_ESTRATEGICOS`

### `test_auto.py`
**Qué hace**: Ejecuta el bot en modo automático (sin inputs) para pruebas
**Cuándo usar**: Pruebas locales sin intervención manual

---

## 📦 Carpeta `bot/` (Código Principal)

### `bot/__init__.py`
**Qué hace**: Exporta las clases principales para importar fácilmente
**No modificar**: Solo exporta, no tiene lógica

### `bot/config.py`
**Qué hace**: Configuración centralizada (límites, URLs, delays)
**Modificar si**: Quieres cambiar límites, porcentajes, delays

### `bot/ai_assistant.py`
**Qué hace**: Analiza proyectos con IA y genera propuestas
**Modificar si**: Quieres cambiar el prompt de la IA, modelos

### `bot/workana_bot.py`
**Qué hace**: Lógica principal (scraping, login, envío de propuestas)
**Modificar si**: Quieres cambiar selectores, comportamiento del bot

---

## 🛠️ Archivos de Configuración

### `requirements.txt`
**Qué hace**: Lista de dependencias Python
**Modificar si**: Agregas nuevas librerías

### `.env`
**Qué hace**: Credenciales y configuración (NO subir a GitHub)
**Crear manualmente**: Con tus credenciales
**Contenido**:
```
WORKANA_EMAIL=...
WORKANA_PASS=...
GEMINI_KEY=...
HEADLESS_MODE=true
AUTO_MODE=true
SPEED_MODE=safe
```

### `.gitignore`
**Qué hace**: Archivos que Git debe ignorar
**No modificar**: Ya configurado correctamente

---

## 📚 Carpeta `docs/` (Documentación)

### `docs/DEPLOY_VPS.md`
**Qué hace**: Guía completa de deployment (detallada)
**Cuándo leer**: Si necesitas detalles técnicos

### `docs/ESTRATEGIA.md`
**Qué hace**: Análisis de estrategia y recomendaciones
**Cuándo leer**: Para entender mejor el bot

### `docs/VPS_RECOMENDACIONES.md`
**Qué hace**: Comparativa de VPS
**Cuándo leer**: Antes de contratar VPS

---

## 🚀 Archivos de Deployment

### `setup_vps.sh`
**Qué hace**: Script que instala todo automáticamente en VPS
**Cuándo usar**: Primera vez en VPS
**Ejecutar**: `chmod +x setup_vps.sh && ./setup_vps.sh`

### `GUIA_VPS.md`
**Qué hace**: Guía rápida paso a paso para VPS
**Cuándo leer**: Para subir a VPS (LEER ESTE PRIMERO)

---

## 💾 Carpeta `data/` (Datos Persistentes)

### `data/workana_cookies.pkl`
**Qué hace**: Cookies de sesión guardadas
**Generado automáticamente**: No tocar manualmente

### `data/history_proposals.json`
**Qué hace**: Historial de proyectos ya procesados
**Generado automáticamente**: No tocar manualmente

---

## 🗑️ Archivos que NO Debes Tocar

- `chrome_profile/` - Perfil de Chrome (generado automáticamente)
- `__pycache__/` - Cache de Python (se regenera)
- `.git/` - Control de versiones (si usas Git)

---

## 📝 Resumen Rápido

**Para cambiar configuración**: `bot/config.py`
**Para cambiar horarios**: `scheduler.py`
**Para cambiar lógica del bot**: `bot/workana_bot.py`
**Para cambiar prompt IA**: `bot/ai_assistant.py`
**Para subir a VPS**: Leer `GUIA_VPS.md`
