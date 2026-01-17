# 🚀 Guía de Despliegue al VPS

Como estamos usando Git, el proceso es muy limpio. No necesitas copiar archivos manualmente.

## 1. Subir cambios desde tu PC (Local)

Primero, guarda los cambios que acabamos de hacer y súbelos a GitHub.

Abre una terminal en la carpeta del bot (`c:\Users\branc\Escritorio\bot_workana`) y ejecuta:

```powershell
# 1. Agregar los archivos nuevos/modificados
git add .

# 2. Guardar el commit
git commit -m "Implementacion de logs y limites semanales"

# 3. Subir a GitHub
git push
```

---

## 2. Actualizar el VPS (Remoto)

Ahora conéctate a tu servidor VPS.

### A. Conectar por SSH
```bash
ssh root@TU_IP_DEL_VPS
```

### B. Descargar cambios
Ve a la carpeta donde tienes el bot (ejemplo: `bot_workana`):

```bash
cd bot_workana

# Descargar lo último de GitHub
git pull
```

### C. Actualizar dependencias
Como actualizamos `requirements.txt` (es importante hacer esto por la librería de IA):

```bash
# Activar entorno virtual (si usas uno)
# source venv/bin/activate

pip install -r requirements.txt
```

### D. Reiniciar el Bot
Para que tome los cambios, debes detener el proceso anterior y arrancar el nuevo.

**Si lo ejecutas con `screen` o terminal simple:**
1. Busca el proceso: `ps aux | grep scheduler.py`
2. Mátalo: `kill -9 ID_DEL_PROCESO`
3. Inicia de nuevo:
   ```bash
   nohup python3 scheduler.py > /dev/null 2>&1 &
   ```
   *(Nota: Ya no necesitamos redirigir logs aquí porque el bot ahora los guarda internamente en la carpeta `logs/`)*

**Si usas `systemd` (recomendado):**
```bash
sudo systemctl restart bot_workana
```

---

## 3. Verificar que funciona

Unos segundos después de reiniciar, verifica que se creó el log:

```bash
tail -f logs/bot_execution.log
```

Deberías ver el mensaje de inicio:
`[FECHA] [INFO] 🚀 Iniciando ejecución programada...`
