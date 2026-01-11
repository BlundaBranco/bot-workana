"""
Punto de entrada principal del bot de Workana.

Ejecuta el bot y maneja la inicialización.
"""

from bot import WorkanaBot


if __name__ == "__main__":
    bot = WorkanaBot()
    bot.run()
