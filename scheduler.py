"""
Programador de ejecuciones del bot.

Ejecuta el bot en horarios estratégicos para maximizar las oportunidades.
Configurado para 52 propuestas por semana (7-8 por día).
"""

import schedule
import time
from datetime import datetime
from bot import WorkanaBot

# Horarios estratégicos para 52 propuestas/semana
# 52 propuestas / 5 días = ~10-11 propuestas/día
# 2 ejecuciones de 5-6 propuestas cada una = perfecto
# ⚠️ IMPORTANTE: Estos horarios usan la ZONA HORARIA del VPS
# Verifica con: timedatectl
# Cambia con: sudo timedatectl set-timezone America/Argentina/Buenos_Aires
HORARIOS_ESTRATEGICOS = [
    "09:00",  # Mañana (clientes revisando proyectos) - Zona horaria del VPS
    "17:00",  # Tarde (máxima actividad) - Zona horaria del VPS
]

# Días de la semana (0=Lunes, 6=Domingo)
# Ejecutar de lunes a viernes (días laborables)
DIAS_ESTRATEGICOS = [0, 1, 2, 3, 4]  # Lunes a Viernes


def ejecutar_bot():
    """Ejecuta el bot una vez."""
    print(f"\n{'='*60}")
    print(f"🚀 Iniciando bot - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")
    
    try:
        bot = WorkanaBot()
        bot.run()
    except Exception as e:
        print(f"❌ Error ejecutando bot: {e}")
        import traceback
        traceback.print_exc()
    
    print(f"\n✅ Ejecución completada - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")


def configurar_horarios():
    """Configura los horarios de ejecución."""
    for hora in HORARIOS_ESTRATEGICOS:
        # Ejecutar solo en días laborables
        schedule.every().monday.at(hora).do(ejecutar_bot)
        schedule.every().tuesday.at(hora).do(ejecutar_bot)
        schedule.every().wednesday.at(hora).do(ejecutar_bot)
        schedule.every().thursday.at(hora).do(ejecutar_bot)
        schedule.every().friday.at(hora).do(ejecutar_bot)
    
    # Obtener zona horaria actual
    import subprocess
    try:
        timezone = subprocess.check_output(['timedatectl', 'show', '--property=Timezone', '--value']).decode().strip()
    except:
        timezone = "UTC (verificar con: timedatectl)"
    
    print("📅 Horarios configurados:")
    for hora in HORARIOS_ESTRATEGICOS:
        print(f"   - Lunes a Viernes a las {hora} ({timezone})")


def main():
    """Función principal del scheduler."""
    print("="*60)
    print("🤖 SCHEDULER DEL BOT DE WORKANA")
    print("="*60)
    print(f"⏰ Iniciado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📊 Objetivo: 52 propuestas por semana")
    print(f"📅 Ejecuciones: 2 veces al día (09:00 y 17:00)")
    print(f"📈 Propuestas por ejecución: 5-6 (límite 7)")
    print("="*60)
    
    configurar_horarios()
    
    print("\n✅ Scheduler activo. Esperando horarios programados...")
    print("   Presiona Ctrl+C para detener.\n")
    
    # Ejecutar inmediatamente la primera vez (opcional)
    # ejecutar_bot()
    
    # Loop principal
    while True:
        schedule.run_pending()
        time.sleep(60)  # Verificar cada minuto


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Scheduler detenido por el usuario.")
    except Exception as e:
        print(f"\n❌ Error fatal: {e}")
        import traceback
        traceback.print_exc()
