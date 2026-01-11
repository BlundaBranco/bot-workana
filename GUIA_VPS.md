# 🚀 Guía VPS - Paso a Paso (Super Directa)

## ✅ ¿Subir a GitHub? ¿Usar Docker?

### **GitHub: SÍ** (Recomendado)
- ✅ Fácil hacer cambios: `git push` → `git pull` en VPS
- ✅ Backup automático
- ✅ Control de versiones
- ⚠️ **NO subas el `.env`** (está en `.gitignore`)

### **Docker: NO necesario**
- ❌ Más complejo para este caso
- ✅ Python directo es más simple
- ✅ Menos recursos

---

## 📋 PASOS PARA SUBIR A VPS

### **PASO 1: Subir a GitHub** (Opcional pero recomendado)

```bash
# En tu PC local
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/tu-usuario/bot-workana.git
git push -u origin main
```

### **PASO 2: Contratar VPS**

**Recomendado: Contabo** (€4.99/mes)
1. Ir a https://contabo.com
2. Elegir "VPS S" (4GB RAM)
3. OS: Ubuntu 22.04
4. Pagar y esperar 5 min

### **PASO 3: Conectarte al VPS**

```bash
ssh root@tu_vps_ip
# O si creaste usuario:
ssh usuario@tu_vps_ip
```

### **PASO 4: Instalar Todo**

```bash
# Opción A: Desde GitHub (recomendado)
git clone https://github.com/tu-usuario/bot-workana.git
cd bot-workana
chmod +x setup_vps.sh
./setup_vps.sh

# Opción B: Manual
sudo apt update && sudo apt upgrade -y
sudo apt install python3 python3-pip git -y
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
sudo apt-get install -f -y
pip3 install -r requirements.txt
```

### **PASO 5: Configurar .env**

```bash
nano .env
```

Pegar:
```env
WORKANA_EMAIL=tu_email@ejemplo.com
WORKANA_PASS=tu_password
GEMINI_KEY=tu_api_key_gemini
HEADLESS_MODE=true
AUTO_MODE=true
SPEED_MODE=safe
```

Guardar: `Ctrl+X`, luego `Y`, luego `Enter`

### **PASO 6: Configurar como Servicio**

```bash
sudo nano /etc/systemd/system/workana-bot.service
```

Pegar (ajusta `tu_usuario` y rutas):
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

Activar:
```bash
sudo systemctl daemon-reload
sudo systemctl enable workana-bot
sudo systemctl start workana-bot
sudo systemctl status workana-bot
```

### **PASO 7: Verificar que Funciona**

```bash
# Ver logs en tiempo real
sudo journalctl -u workana-bot -f

# Ver últimos logs
sudo journalctl -u workana-bot -n 50
```

---

## 🔄 HACER CAMBIOS DESPUÉS

### **Si usas GitHub:**

```bash
# En tu PC local: hacer cambios
git add .
git commit -m "Descripción del cambio"
git push

# En el VPS: actualizar
cd bot-workana
git pull
sudo systemctl restart workana-bot
```

### **Si NO usas GitHub:**

```bash
# Opción 1: Editar directamente en VPS
nano bot/workana_bot.py  # o el archivo que quieras
sudo systemctl restart workana-bot

# Opción 2: Subir archivo con SCP (desde tu PC)
scp bot/workana_bot.py usuario@vps_ip:/root/bot-workana/bot/
ssh usuario@vps_ip
sudo systemctl restart workana-bot
```

---

## ⚙️ CONFIGURACIÓN: 52 Propuestas/Semana

**Configuración actual en `scheduler.py`:**
- **2 ejecuciones diarias**: 09:00 y 17:00
- **Días**: Lunes a Viernes
- **Propuestas por ejecución**: 5-6 (límite 7)
- **Total**: ~50-52 propuestas/semana

**Para cambiar horarios:**
```bash
nano scheduler.py
# Modifica HORARIOS_ESTRATEGICOS
sudo systemctl restart workana-bot
```

---

## 🐛 Problemas Comunes

### Bot no inicia:
```bash
sudo journalctl -u workana-bot -n 100  # Ver errores
google-chrome --version  # Verificar Chrome
```

### Reiniciar servicio:
```bash
sudo systemctl restart workana-bot
```

### Detener servicio:
```bash
sudo systemctl stop workana-bot
```

---

## ✅ Checklist

- [ ] VPS contratado
- [ ] Código subido (GitHub o manual)
- [ ] Dependencias instaladas
- [ ] Archivo `.env` creado
- [ ] Servicio systemd configurado
- [ ] Servicio iniciado y funcionando
- [ ] Logs verificados

**¡Listo! El bot corre automáticamente 24/7** 🚀
