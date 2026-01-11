#!/bin/bash
# Script de instalación automática para VPS (Ubuntu/Debian)

echo "🚀 Instalando dependencias para Workana Bot..."

# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Python y herramientas
sudo apt install -y python3 python3-pip python3-venv git curl wget

# Instalar Chrome
echo "📦 Instalando Google Chrome..."
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
sudo apt-get install -f -y

# Verificar instalación
echo "✅ Chrome instalado:"
google-chrome --version

# Instalar dependencias Python
echo "📦 Instalando dependencias Python..."
pip3 install --upgrade pip
pip3 install -r requirements.txt

echo "✅ Instalación completada!"
echo ""
echo "📝 Próximos pasos:"
echo "1. Crea el archivo .env con tus credenciales"
echo "2. Configura el scheduler como servicio systemd"
echo "3. Revisa DEPLOY_VPS.md para más detalles"
