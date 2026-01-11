"""
Bot de Workana - Módulo principal.

Este paquete contiene todos los módulos del bot:
- config: Configuración centralizada
- ai_assistant: Asistente de IA para análisis y propuestas
- workana_bot: Lógica principal del bot
"""

from .config import Config
from .ai_assistant import AIAssistant
from .workana_bot import WorkanaBot

__all__ = ['Config', 'AIAssistant', 'WorkanaBot']
