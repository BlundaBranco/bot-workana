"""
Script de prueba para modo automático.

Ejecuta el bot en modo automático (sin inputs) para pruebas locales.
"""

import os
from bot import WorkanaBot

# Configurar modo automático y rápido para pruebas
os.environ["AUTO_MODE"] = "true"
os.environ["SPEED_MODE"] = "fast"  # Cambia a "safe" para producción
os.environ["HEADLESS_MODE"] = "false"  # Ver el navegador durante pruebas

if __name__ == "__main__":
    print("🧪 MODO PRUEBA - AUTO MODE ACTIVADO")
    print("=" * 60)
    print("⚠️ El bot se ejecutará automáticamente sin pedir confirmación")
    print("⚠️ Modo rápido activado (2-3x más rápido)")
    print("=" * 60)
    print()
    
    bot = WorkanaBot()
    bot.run()
