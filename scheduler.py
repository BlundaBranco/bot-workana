"""
Programador de ejecuciones del bot.

Ejecuta el bot en horarios estratégicos para maximizar las oportunidades.
Configurado para 52 propuestas por semana (7-8 por día).
"""

import schedule
import time
from datetime import datetime
from bot import WorkanaBot
from bot.logger import logger

# Horarios estratégicos para 52 propuestas/semana
# 52 propuestas / 5 días = ~10-11 propuestas/día
# 2 ejecuciones de 5-6 propuestas cada una = perfecto
# ⚠️ IMPORTANTE: Estos horarios usan la ZONA HORARIA del VPS
# Verifica con: timedatectl
HORARIOS_ESTRATEGICOS = [
    "09:00",  # Mañana (clientes revisando proyectos)
    "17:00",  # Tarde (máxima actividad)
]

# Días de la semana (0=Lunes, 6=Domingo)
DIAS_ESTRATEGICOS = [0, 1, 2, 3, 4]  # Lunes a Viernes


def ejecutar_bot():
    """Ejecuta el bot una vez."""
    logger.info(f"{'='*30}")
    logger.info(f"🚀 Iniciando ejecución programada")
    logger.info(f"{'='*30}")
    
    try:
        bot = WorkanaBot()
        bot.run()
    except Exception as e:
        logger.error(f"❌ Error ejecutando bot: {e}")
        import traceback
        traceback.print_exc()
    
    logger.info("✅ Ejecución completada")


def configurar_horarios():
    """Configura los horarios de ejecución."""
    for hora in HORARIOS_ESTRATEGICOS:
        # Ejecutar solo en días laborables
        schedule.every().monday.at(hora).do(ejecutar_bot)
        schedule.every().tuesday.at(hora).do(ejecutar_bot)
        schedule.every().wednesday.at(hora).do(ejecutar_bot)
        schedule.every().thursday.at(hora).do(ejecutar_bot)
        schedule.every().friday.at(hora).do(ejecutar_bot)
    
    # Obtener zona horaria actual (compatible Windows/Linux)
    try:
        import subprocess
        if hasattr(subprocess, 'check_output'):
            # Intento genérico, fallará silenciosamente en Windows si no existe el comando
            try:
                timezone = subprocess.check_output(['timedatectl', 'show', '--property=Timezone', '--value'], stderr=subprocess.DEVNULL).decode().strip()
            except:
                timezone = time.tzname[0]
        else:
            timezone = time.tzname[0]
    except:
        timezone = "Desconocida"
    
    logger.info("📅 Horarios configurados:")
    for hora in HORARIOS_ESTRATEGICOS:
        logger.info(f"   - Lunes a Viernes a las {hora} ({timezone})")


def main():
    """Función principal del scheduler."""
    logger.info("="*60)
    logger.info("🤖 SCHEDULER DEL BOT DE WORKANA - INICIADO")
    logger.info("="*60)
    logger.info(f"📊 Objetivo: 52 propuestas por semana")
    logger.info(f"📅 Ejecuciones: 2 veces al día (09:00 y 17:00)")
    
    configurar_horarios()
    
    logger.info("✅ Scheduler activo. Esperando horarios programados...")
    logger.info("   Logs disponibles en: logs/bot_execution.log")
    
    # Loop principal
    while True:
        schedule.run_pending()
        time.sleep(60)  # Verificar cada minuto


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("👋 Scheduler detenido por el usuario.")
    except Exception as e:
        logger.critical(f"❌ Error fatal en scheduler: {e}")
