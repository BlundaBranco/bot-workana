# ✅ Verificación y Pruebas del Bot

## 🔍 ¿Qué significa "active (running)"?

**Significa que:**
- ✅ El servicio está activo y corriendo
- ✅ El scheduler está esperando los horarios programados
- ✅ Se ejecutará automáticamente a las 09:00 y 17:00 (Lunes-Viernes)

**PERO:** El bot NO se ejecuta inmediatamente, espera los horarios programados.

---

## 📊 Verificar que Funciona

### 1. Ver Logs en Tiempo Real

```bash
sudo journalctl -u workana-bot -f
```

Esto muestra los logs en tiempo real. Deberías ver algo como:
```
🤖 SCHEDULER DEL BOT DE WORKANA
⏰ Iniciado: 2025-01-11 20:30:00
📅 Ejecuciones: 2 veces al día (09:00 y 17:00)
✅ Scheduler activo. Esperando horarios programados...
```

**Para salir:** Presiona `Ctrl+C`

### 2. Ver Últimos Logs

```bash
sudo journalctl -u workana-bot -n 50
```

Muestra las últimas 50 líneas de logs.

### 3. Ver Estado del Servicio

```bash
sudo systemctl status workana-bot
```

Deberías ver:
- **Active: active (running)**
- **Main PID:** un número
- Sin errores en rojo

---

## 🧪 Probar Manualmente (AHORA)

Si quieres probar que funciona **AHORA MISMO** (sin esperar horarios):

### Opción 1: Ejecutar el Bot Directamente

```bash
cd ~/bot-workana
python3 main.py
```

Esto ejecuta el bot una vez (modo manual).

### Opción 2: Ejecutar el Scheduler con Prueba Inmediata

Edita temporalmente el scheduler:

```bash
cd ~/bot-workana
nano scheduler.py
```

Busca esta línea (alrededor de línea 75):
```python
# ejecutar_bot()  # <-- Descomenta esta línea
```

Quita el `#` para que quede:
```python
ejecutar_bot()  # Ejecutar inmediatamente
```

Guarda (`Ctrl+X`, `Y`, `Enter`) y reinicia:
```bash
sudo systemctl restart workana-bot
sudo journalctl -u workana-bot -f
```

**IMPORTANTE:** Después de probar, vuelve a comentar esa línea para que no se ejecute cada vez que reinicies.

---

## ⏰ ¿Cuándo se Ejecuta?

**Horarios programados:**
- **09:00** (mañana)
- **17:00** (tarde)
- **Días:** Lunes a Viernes
- **Propuestas por ejecución:** 5-6

**Para cambiar horarios:**
```bash
nano scheduler.py
# Modifica HORARIOS_ESTRATEGICOS
sudo systemctl restart workana-bot
```

---

## 🔍 Verificar que Envía Propuestas

### 1. Ver Historial de Propuestas

```bash
cat ~/bot-workana/data/history_proposals.json
```

Muestra todas las URLs de proyectos donde ya ofertaste.

### 2. Contar Propuestas Enviadas

```bash
cat ~/bot-workana/data/history_proposals.json | grep -o "workana.com" | wc -l
```

### 3. Ver Últimas Propuestas

```bash
tail -20 ~/bot-workana/data/history_proposals.json
```

---

## 🐛 Si Hay Problemas

### El bot no se ejecuta en los horarios:

1. **Verificar zona horaria del VPS:**
```bash
timedatectl
```

2. **Cambiar zona horaria si es necesario:**
```bash
sudo timedatectl set-timezone America/Argentina/Buenos_Aires
# O la zona que necesites
```

3. **Verificar que el scheduler está corriendo:**
```bash
sudo systemctl status workana-bot
```

### El bot da errores:

```bash
# Ver errores detallados
sudo journalctl -u workana-bot -n 100 --no-pager

# Ver errores en tiempo real
sudo journalctl -u workana-bot -f
```

### Reiniciar el servicio:

```bash
sudo systemctl restart workana-bot
sudo systemctl status workana-bot
```

---

## ✅ Checklist de Verificación

- [ ] Servicio está "active (running)"
- [ ] Logs muestran "Scheduler activo"
- [ ] Zona horaria correcta
- [ ] Archivo `.env` configurado
- [ ] Chrome instalado y funcionando
- [ ] Prueba manual exitosa (opcional)

---

## 🎯 Próximos Pasos

1. **Dejar el bot corriendo** - Se ejecutará automáticamente
2. **Monitorear logs** ocasionalmente: `sudo journalctl -u workana-bot -n 50`
3. **Verificar propuestas** en Workana manualmente
4. **Ajustar horarios** si es necesario

**¡El bot está funcionando! Solo espera los horarios programados.** 🚀
