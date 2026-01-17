# 📜 Cómo Ver y Verificar Logs en el VPS

Ya está implementado el sistema de logs. Ahora puedes monitorear tu bot como un profesional.

## 1. Dónde están los logs

El bot crea automáticamente una carpeta `logs` y guarda todo en:
`bot_workana/logs/bot_execution.log`

## 2. Cómo ver los datos (Comandos para VPS)

Conéctate a tu VPS por SSH y entra a la carpeta del bot:
```bash
cd bot_workana
```

### 👁️ Ver los últimos eventos (Tiempo Real)
Este es el comando más útil. Te muestra lo que está pasando **ahora mismo**:
```bash
tail -f logs/bot_execution.log
```
*(Presiona `Ctrl+C` para salir)*

### 📄 Ver todo el archivo
```bash
cat logs/bot_execution.log
```

### 🔍 Buscar errores específicos
Si quieres saber si algo falló:
```bash
grep "ERROR" logs/bot_execution.log
```

---

## 3. Verificar el Límite Semanal

El bot ahora cuenta cuántas propuestas has enviado desde el Lunes a las 00:00.

### Cómo comprobar el conteo
Cada vez que el bot arranca, verás una línea en el log como esta:
`[2024-01-16 10:00:00] [INFO] 📊 Propuestas de esta semana: 12/52`

### Prueba Manual (Simulación)
Si quieres probar que el límite funciona SIN esperar a enviar 52 propuestas:

1.  Abre `bot/config.py`
2.  Cambia temporalmente:
    ```python
    MAX_PROPOSALS_PER_WEEK = 0  # Poner 0 o 1 para probar
    ```
3.  Ejecuta el test automático:
    ```bash
    python test_auto.py
    ```
4.  Deberías ver en el log:
    `[WARNING] 🛑 LÍMITE SEMANAL ALCANZADO (X/0). Deteniendo ejecución.`

---

## 4. Verificar Ejecución del Scheduler

Para asegurarte de que el scheduler está corriendo en segundo plano en tu VPS (si usaste `nohup` o `systemd`):

```bash
ps aux | grep scheduler.py
```

Si aparece en la lista, ¡está vivo y esperando su hora! Su actividad quedará registrada en el mismo archivo de logs.
