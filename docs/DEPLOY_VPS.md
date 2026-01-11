# 🚀 Guía de Deployment en VPS

## 📊 Resumen de Requisitos

- **Propuestas objetivo**: 52 por semana (~7-8 por día)
- **Horarios**: 5 ejecuciones diarias (Lunes-Viernes)
- **Recursos necesarios**: 2GB RAM, 1 CPU, 20GB disco

---

## 💰 Recomendación de VPS (Calidad/Precio)

### 🥇 **RECOMENDADO: Contabo** 
- **Precio**: €4.99/mes (~$5.50 USD)
- **Especificaciones**: 4GB RAM, 2 CPU, 200GB SSD
- **Ubicación**: Alemania (buena latencia para Workana)
- **Link**: https://contabo.com
- **✅ Ventajas**: 
  - Excelente relación precio/rendimiento
  - Muy estable
  - Soporte en español
  - Sin límites de ancho de banda

### 🥈 **Alternativa: Hetzner**
- **Precio**: €4.15/mes (~$4.50 USD)
- **Especificaciones**: 2GB RAM, 1 CPU, 20GB SSD
- **Ubicación**: Alemania
- **Link**: https://hetzner.com
- **✅ Ventajas**: Más barato, muy confiable

### 🥉 **Alternativa: DigitalOcean**
- **Precio**: $6/mes
- **Especificaciones**: 1GB RAM, 1 CPU, 25GB SSD
- **Ubicación**: Múltiples (elige más cercano)
- **Link**: https://digitalocean.com
- **✅ Ventajas**: Muy fácil de usar, buena documentación

### 🆓 **Opción Gratis: Oracle Cloud**
- **Precio**: $0/mes (siempre gratis)
- **Especificaciones**: 1GB RAM, 1 CPU, 50GB SSD
- **⚠️ Desventajas**: 
  - Más difícil de configurar
  - Puede ser lento
  - Límites de recursos

---

## 💵 Costos Estimados

### **Mensual:**
- **VPS**: $5-6 USD/mes (Contabo recomendado)
- **API Gemini**: ~$0-5 USD/mes (depende del uso)
  - Gemini Flash es muy barato
  - ~1000 requests/mes = ~$1-2 USD
- **Total**: **$6-11 USD/mes** (~$72-132 USD/año)

### **Anual:**
- **VPS**: $60-72 USD/año
- **API**: $12-24 USD/año
- **Total**: **$72-96 USD/año**

### **ROI (Retorno de Inversión):**
Si consigues **1 proyecto de $500/mes**, el ROI es **50x** 🚀

---

## 📋 Pasos para Deployment

### 1. **Preparar el código localmente**

```bash
# Asegúrate de tener todo listo
python main.py  # Prueba que funcione
```

### 2. **Crear archivo .env para VPS**

```env
WORKANA_EMAIL=tu_email@ejemplo.com
WORKANA_PASS=tu_password
GEMINI_KEY=tu_api_key_gemini
HEADLESS_MODE=true
```

### 3. **Subir a VPS**

Opciones:
- **Git**: `git push` y luego `git pull` en VPS
- **SCP**: `scp -r bot_workana/ user@vps:/home/user/`
- **FTP/SFTP**: Usa FileZilla o similar

### 4. **Configurar VPS (Ubuntu/Debian)**

```bash
# Conectarte al VPS
ssh user@tu_vps_ip

# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Python y dependencias
sudo apt install python3 python3-pip git -y

# Instalar Chrome/Chromium para Selenium
sudo apt install chromium-browser chromium-chromedriver -y

# O usar Chrome (mejor para undetected_chromedriver)
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
sudo apt-get install -f

# Clonar o subir tu código
cd ~
git clone tu_repo  # o subir archivos manualmente
cd bot_workana

# Instalar dependencias Python
pip3 install -r requirements.txt
pip3 install schedule  # Para el scheduler

# Crear archivo .env
nano .env  # Pegar tus credenciales
```

### 5. **Configurar el Scheduler**

```bash
# Instalar como servicio systemd
sudo nano /etc/systemd/system/workana-bot.service
```

Contenido del servicio:
```ini
[Unit]
Description=Workana Bot Scheduler
After=network.target

[Service]
Type=simple
User=tu_usuario
WorkingDirectory=/home/tu_usuario/bot_workana
Environment="PATH=/usr/bin:/usr/local/bin"
ExecStart=/usr/bin/python3 /home/tu_usuario/bot_workana/scheduler.py
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
sudo systemctl status workana-bot  # Verificar que funciona
```

### 6. **Ver logs**

```bash
# Ver logs en tiempo real
sudo journalctl -u workana-bot -f

# Ver últimos logs
sudo journalctl -u workana-bot -n 100
```

---

## ⚙️ Configuración de Horarios

El archivo `scheduler.py` está configurado para:
- **5 ejecuciones diarias**: 08:00, 11:00, 14:00, 17:00, 20:00
- **Días**: Lunes a Viernes
- **Total**: ~25 ejecuciones/semana
- **Propuestas**: ~7-8 por día (límite de 7 por ejecución)

### Ajustar horarios:

Edita `scheduler.py` y modifica `HORARIOS_ESTRATEGICOS`:
```python
HORARIOS_ESTRATEGICOS = [
    "09:00",  # Cambia a tu zona horaria
    "12:00",
    # ... etc
```

---

## 🔒 Seguridad

1. **No subas el .env a Git**
   - Agrega `.env` a `.gitignore`
   
2. **Permisos del archivo .env**
   ```bash
   chmod 600 .env
   ```

3. **Firewall**
   ```bash
   sudo ufw allow 22  # SSH
   sudo ufw enable
   ```

---

## 🐛 Troubleshooting

### Bot no inicia:
```bash
# Verificar que Chrome está instalado
google-chrome --version

# Verificar dependencias
pip3 list | grep selenium
```

### Scheduler no funciona:
```bash
# Ver logs
sudo journalctl -u workana-bot -f

# Reiniciar servicio
sudo systemctl restart workana-bot
```

### Error de permisos:
```bash
# Dar permisos a chrome_profile
chmod -R 755 chrome_profile/
```

---

## 📊 Monitoreo

### Ver estadísticas:
```bash
# Ver historial de propuestas
cat data/history_proposals.json | wc -l

# Ver últimas propuestas
tail -20 data/history_proposals.json
```

### Alertas (opcional):
Puedes configurar email/Slack cuando el bot falle usando servicios como:
- **Cronitor**: Monitoreo de cron jobs
- **UptimeRobot**: Monitoreo de servicios

---

## ✅ Checklist Pre-Deployment

- [ ] Código probado localmente
- [ ] Archivo .env creado con credenciales
- [ ] VPS contratado y configurado
- [ ] Chrome instalado en VPS
- [ ] Dependencias Python instaladas
- [ ] Scheduler configurado como servicio
- [ ] Logs funcionando
- [ ] Prueba de ejecución manual exitosa

---

## 🎯 Resultado Esperado

Con esta configuración:
- **52 propuestas/semana** enviadas automáticamente
- **Ejecución 24/7** sin necesidad de PC
- **Costo**: ~$6-11 USD/mes
- **ROI**: Muy alto si consigues proyectos

¡Éxito con tu bot! 🚀
