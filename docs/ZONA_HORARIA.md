# ⏰ Configuración de Zona Horaria

## ❓ ¿De qué país son las horas?

Los horarios en `scheduler.py` (09:00 y 17:00) usan la **zona horaria del VPS**.

Por defecto, DigitalOcean usa **UTC** (hora de Londres, sin horario de verano).

---

## 🔍 Verificar Zona Horaria Actual

```bash
timedatectl
```

O solo la zona:
```bash
timedatectl show --property=Timezone --value
```

---

## 🌍 Cambiar Zona Horaria

### Ejemplos comunes:

**Argentina:**
```bash
sudo timedatectl set-timezone America/Argentina/Buenos_Aires
```

**España:**
```bash
sudo timedatectl set-timezone Europe/Madrid
```

**México:**
```bash
sudo timedatectl set-timezone America/Mexico_City
```

**Colombia:**
```bash
sudo timedatectl set-timezone America/Bogota
```

**Chile:**
```bash
sudo timedatectl set-timezone America/Santiago
```

### Ver todas las zonas disponibles:

```bash
timedatectl list-timezones | grep America
# O
timedatectl list-timezones | grep Europe
```

---

## 📊 Conversión de Horarios

Si tu VPS está en **UTC** y quieres que se ejecute a las 09:00 de **Argentina**:

- **Argentina (UTC-3)**: 09:00 Argentina = 12:00 UTC
- **España (UTC+1)**: 09:00 España = 08:00 UTC

**Solución:** Cambia la zona horaria del VPS a la tuya, o ajusta los horarios en `scheduler.py`.

---

## ⚙️ Ajustar Horarios en scheduler.py

Si prefieres mantener UTC pero ajustar las horas:

```bash
nano scheduler.py
```

Cambia:
```python
HORARIOS_ESTRATEGICOS = [
    "12:00",  # 09:00 Argentina (UTC-3)
    "20:00",  # 17:00 Argentina (UTC-3)
]
```

Luego:
```bash
sudo systemctl restart workana-bot
```

---

## ✅ Verificar que Funciona

Después de cambiar la zona horaria:

```bash
# Ver hora actual
date

# Ver zona horaria
timedatectl

# Ver próximos horarios programados (en los logs)
sudo journalctl -u workana-bot -n 20
```

---

## 🎯 Recomendación

**Mejor opción:** Cambiar la zona horaria del VPS a la tuya:

```bash
sudo timedatectl set-timezone America/Argentina/Buenos_Aires
# O la zona que necesites
```

Así los horarios 09:00 y 17:00 serán en tu hora local, más fácil de entender.

---

## 📝 Ejemplo Completo

```bash
# 1. Ver zona actual
timedatectl
# Output: Timezone: UTC

# 2. Cambiar a Argentina
sudo timedatectl set-timezone America/Argentina/Buenos_Aires

# 3. Verificar
date
# Output: Sat Jan 11 20:30:00 ART 2025

# 4. Reiniciar servicio
sudo systemctl restart workana-bot

# 5. Ver logs
sudo journalctl -u workana-bot -f
# Deberías ver: "Lunes a Viernes a las 09:00 (America/Argentina/Buenos_Aires)"
```
