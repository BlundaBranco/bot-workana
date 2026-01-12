# 🐛 Debug: Bot se Queda en "Cargando Cookies"

## ❌ El Problema

El bot se queda en "🔑 Intentando cargar cookies guardadas..." y no avanza.

---

## 🔍 Diagnóstico

### 1. Verificar que las Cookies Existen

```bash
# En el VPS
ls -la ~/bot-workana/data/workana_cookies.pkl
```

Si no existe o está vacío, necesitas subir las cookies.

### 2. Ver Logs Detallados

```bash
sudo journalctl -u workana-bot -f
```

Busca mensajes como:
- "📄 Página cargada"
- "📂 Leyendo archivo de cookies"
- "🍪 Cargando X cookies"
- Errores en rojo

### 3. Verificar Tamaño del Archivo

```bash
# Si el archivo es muy pequeño (< 100 bytes), está vacío o corrupto
du -h ~/bot-workana/data/workana_cookies.pkl
```

---

## ✅ Soluciones

### Solución 1: Las Cookies No Existen o Están Vacías

**Síntoma:** El archivo no existe o es muy pequeño.

**Solución:**
1. En tu PC local, hacer login y guardar cookies
2. Subir al VPS:
```bash
scp data/workana_cookies.pkl root@157.230.134.177:/root/bot-workana/data/
```

### Solución 2: Las Cookies Están Corruptas

**Síntoma:** El archivo existe pero da error al leerlo.

**Solución:**
1. Eliminar cookies viejas:
```bash
rm ~/bot-workana/data/workana_cookies.pkl
```

2. Subir cookies frescas desde tu PC

### Solución 3: Chrome se Queda Cargando

**Síntoma:** Se queda en "Página cargada" y no avanza.

**Solución:**
1. Verificar que Chrome funciona:
```bash
google-chrome --version
google-chrome --headless --disable-gpu --dump-dom https://www.workana.com
```

2. Si Chrome no responde, reiniciar:
```bash
sudo systemctl restart workana-bot
```

### Solución 4: Timeout en la Carga

**Síntoma:** Se queda esperando indefinidamente.

**Solución Temporal:** Aumentar timeout o desactivar headless temporalmente.

---

## 🧪 Prueba Manual

Para probar si las cookies funcionan:

```bash
cd ~/bot-workana
python3 -c "
import pickle
import os
from bot.config import Config

if os.path.exists(Config.COOKIES_FILE):
    with open(Config.COOKIES_FILE, 'rb') as f:
        cookies = pickle.load(f)
    print(f'✅ Cookies encontradas: {len(cookies)} cookies')
    for c in cookies[:3]:
        print(f'   - {c.get(\"name\", \"N/A\")}: {c.get(\"domain\", \"N/A\")}')
else:
    print('❌ Archivo de cookies no existe')
"
```

---

## 🔄 Reiniciar desde Cero

Si nada funciona:

```bash
# 1. Detener servicio
sudo systemctl stop workana-bot

# 2. Eliminar cookies viejas
rm ~/bot-workana/data/workana_cookies.pkl

# 3. Subir cookies frescas desde tu PC
# (desde tu PC local)
scp data/workana_cookies.pkl root@157.230.134.177:/root/bot-workana/data/

# 4. Reiniciar servicio
sudo systemctl start workana-bot

# 5. Ver logs
sudo journalctl -u workana-bot -f
```

---

## 📝 Logs Mejorados

El código ahora muestra más información:
- "📄 Página cargada"
- "📂 Leyendo archivo de cookies"
- "🍪 Cargando X cookies"
- "✅ X/Y cookies cargadas"
- "🔄 Recargando página"
- "🔍 Verificando si el login funcionó"

Si se queda en alguno de estos pasos, sabrás exactamente dónde.

---

## ⚠️ Nota sobre Headless

En modo headless, si las cookies no funcionan, el bot **NO puede hacer login manual** porque no hay interfaz gráfica.

**Solución obligatoria:** Exportar cookies desde tu PC local.

Ver: `docs/SOLUCION_LOGIN.md`
