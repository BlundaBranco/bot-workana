# Plan de Implementación: Logs y Límite Semanal

Este plan aborda dos mejoras críticas solicitadas: visibilidad de logs en el VPS y cumplimiento del límite semanal de propuestas.

## 1. Sistema de Logs (Logging)

Actualmente, el bot usa `print()`, lo que hace difícil ver el historial de ejecución en segundo plano (VPS).

### Cambios Propuestos
*   **Crear `bot/logger.py`**: Un módulo centralizado para configurar logs.
*   **Archivo de logs**: `logs/bot_execution.log` (con rotación: máximo 5MB, backup de 2 archivos).
*   **Formato**: `[FECHA HORA] [NIVEL] Mensaje`
*   **Integración**: Reemplazar `print` críticos con `logger.info`, `logger.error`, etc. en `workana_bot.py`, `ai_assistant.py` y `scheduler.py`.

## 2. Límite Semanal (52 Propuestas)

Actualmente, `history_proposals.json` es una lista simple de URLs `["url1", "url2"]`, lo que impide saber *cuándo* se enviaron.

### Cambios Propuestos
*   **Migrar esquema de datos**: Cambiar de lista de strings a lista de objetos:
    ```json
    [
      {"url": "http://...", "timestamp": "2024-01-16T10:00:00", "price": 100},
      ...
    ]
    ```
*   **Compatibilidad**: Al cargar, si detecta el formato antiguo (strings), lo mantiene solo para evitar duplicados, pero las nuevas se guardan con fecha.
*   **Lógica de Verificación**:
    *   Función `get_weekly_count()`: Cuenta propuestas enviadas en la semana actual (Lunes-Domingo).
    *   En `run()`: Verificar `if weekly_count >= Config.MAX_PROPOSALS_PER_WEEK: Stop`.

## 3. Archivos a Modificar

#### [MODIFY] [workana_bot.py](file:///c:/Users/branc/Escritorio/bot_workana/bot/workana_bot.py)
*   Integrar `logger`.
*   Actualizar `load_history` para manejar el nuevo formato.
*   Actualizar `save_to_history` para guardar timestamp.
*   Agregar chequeo de límite semanal antes de cada propuesta.

#### [NEW] [logger.py](file:///c:/Users/branc/Escritorio/bot_workana/bot/logger.py)
*   Configuración de `logging` con `RotatingFileHandler`.

#### [MODIFY] [scheduler.py](file:///c:/Users/branc/Escritorio/bot_workana/scheduler.py)
*   Usar logger para registrar ejecuciones programadas.

#### [MODIFY] [requirements.txt](file:///c:/Users/branc/Escritorio/bot_workana/requirements.txt)
*   Asegurar que no falte nada (logging es nativo).

## 4. Verificación
*   Ejecutar `test_auto.py` (o similar) para verificar que se crea la carpeta `logs/` y el archivo `.log`.
*   Verificar que el JSON de historial se actualiza con fechas.
