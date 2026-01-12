# 🚀 Guía DigitalOcean - Paso a Paso

## 📋 PASO 1: Crear VPS en DigitalOcean

1. **Ir a**: https://digitalocean.com
2. **Crear cuenta** (si no tienes)
3. **Crear Droplet**:
   - **Plan**: Basic ($6/mes - 1GB RAM)
   - **Región**: Elige la más cercana a ti
   - **Imagen**: Ubuntu 22.04 (LTS)
   - **Autenticación**: SSH Key (recomendado) o Password
4. **Crear** y esperar 1 minuto

---

## 📋 PASO 2: Conectarte al VPS

```bash
# DigitalOcean te da la IP y el usuario (root)
ssh root@tu_ip_digitalocean

# Si usas SSH Key, se conecta automáticamente
# Si usas Password, te pedirá la contraseña
```

---

## 📋 PASO 3: Instalar Dependencias

```bash
# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Python y herramientas
sudo apt install -y python3 python3-pip git curl wget

# Instalar Chrome
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
sudo apt-get install -f -y

# Verificar Chrome
google-chrome --version
```

---

## 📋 PASO 4: Subir Código (GitHub Recomendado)

### **Opción A: Desde GitHub** (Recomendado)

```bash
# En tu PC local primero:
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/tu-usuario/bot-workana.git
git push -u origin main

# Luego en el VPS:
cd ~
git clone https://github.com/tu-usuario/bot-workana.git
cd bot-workana
```

### **Opción B: Manual (SCP)**

```bash
# Desde tu PC local:
scp -r bot_workana/* root@tu_ip:/root/bot-workana/

# Luego en VPS:
cd ~
mkdir bot-workana
cd bot-workana
```

---

## 📋 PASO 5: Instalar Dependencias Python

```bash
cd bot-workana
pip3 install --upgrade pip
pip3 install -r requirements.txt
```

---

## 📋 PASO 6: Configurar .env

```bash
nano .env
```

Pegar (reemplaza con tus datos):
```env
WORKANA_EMAIL=tu_email@ejemplo.com
WORKANA_PASS=tu_password
GEMINI_KEY=tu_api_key_gemini
HEADLESS_MODE=true
AUTO_MODE=true
SPEED_MODE=safe
```

Guardar: `Ctrl+X`, `Y`, `Enter`

---

## 📋 PASO 7: Configurar como Servicio

```bash
sudo nano /etc/systemd/system/workana-bot.service
```

Pegar (ajusta la ruta si cambiaste de ubicación):
```ini
[Unit]
Description=Workana Bot Scheduler
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/bot-workana
Environment="PATH=/usr/bin:/usr/local/bin"
ExecStart=/usr/bin/python3 /root/bot-workana/scheduler.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Activar servicio:
```bash
sudo systemctl daemon-reload
sudo systemctl enable workana-bot
sudo systemctl start workana-bot
sudo systemctl status workana-bot
```

Si ves "active (running)" → ✅ **¡Funciona!**

---

## 📋 PASO 8: Verificar que Funciona

```bash
# Ver logs en tiempo real
sudo journalctl -u workana-bot -f
```

Deberías ver:
```
🤖 SCHEDULER DEL BOT DE WORKANA
⏰ Iniciado: ...
📅 Ejecuciones: 2 veces al día (09:00 y 17:00)
✅ Scheduler activo. Esperando horarios programados...
```

**Salir:** `Ctrl+C`

### 🧪 Probar AHORA (sin esperar horarios)

```bash
cd ~/bot-workana
python3 main.py
```

Esto ejecuta el bot una vez para probar.

**Nota:** El bot se ejecuta automáticamente a las **09:00** y **17:00** (Lunes-Viernes). Si quieres probarlo ahora, usa el comando de arriba.

**Ver más detalles:** `docs/VERIFICACION.md`

---

## 🔄 HACER CAMBIOS DESPUÉS

### **Con GitHub** (Recomendado):

```bash
# En tu PC: hacer cambios y subir
git add .
git commit -m "Descripción del cambio"
git push

# En VPS: actualizar
cd ~/bot-workana
git pull
sudo systemctl restart workana-bot
```

### **Sin GitHub**:

```bash
# Editar directamente en VPS
nano bot/workana_bot.py  # o el archivo que quieras
sudo systemctl restart workana-bot
```

---

## ⚙️ CONFIGURACIÓN: 52 Propuestas/Semana

**Actual:**
- **2 ejecuciones/día**: 09:00 y 17:00
- **Zona horaria**: La del VPS (por defecto UTC)
- **Días**: Lunes a Viernes
- **Propuestas/ejecución**: 5-6
- **Total**: ~50-52/semana

**⚠️ IMPORTANTE - Configurar Zona Horaria:**

```bash
# Ver zona horaria actual
timedatectl

# Cambiar a tu zona (ejemplo Argentina)
sudo timedatectl set-timezone America/Argentina/Buenos_Aires

# Reiniciar servicio
sudo systemctl restart workana-bot
```

**Ver más:** `docs/ZONA_HORARIA.md`

**Cambiar horarios:**
```bash
nano scheduler.py
# Modifica HORARIOS_ESTRATEGICOS
sudo systemctl restart workana-bot
```

---

## 🐛 Problemas Comunes

### Error de Login (Headless)

Si ves "LOGIN MANUAL REQUERIDO" en modo headless:

**Solución:** Exportar cookies desde tu PC local:

```bash
# En tu PC: hacer login y guardar cookies (HEADLESS_MODE=false)
# Luego subir al VPS:
scp data/workana_cookies.pkl root@157.230.134.177:/root/bot-workana/data/

# En VPS: reiniciar
sudo systemctl restart workana-bot
```

**Ver más:** `docs/SOLUCION_LOGIN.md`

### Bot no inicia:
```bash
sudo journalctl -u workana-bot -n 100  # Ver errores
google-chrome --version  # Verificar Chrome
```

### Reiniciar:
```bash
sudo systemctl restart workana-bot
```

### Detener:
```bash
sudo systemctl stop workana-bot
```

---

## ✅ Checklist

- [ ] VPS creado en DigitalOcean
- [ ] Conectado por SSH
- [ ] Chrome instalado
- [ ] Código subido (GitHub o manual)
- [ ] Dependencias Python instaladas
- [ ] Archivo `.env` creado
- [ ] Servicio systemd configurado y activo
- [ ] Logs verificados

**¡Listo! El bot corre automáticamente 24/7** 🚀
