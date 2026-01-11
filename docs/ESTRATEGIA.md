# 📊 Análisis de Estrategia del Bot de Workana

## 1. Criterios de Aceptación/Rechazo de Propuestas

El bot usa **múltiples filtros** para decidir si ofertar o no:

### Filtros Automáticos (antes de la IA):
1. **Historial**: Si ya ofertaste a ese proyecto → ❌ Rechazado
2. **Rating del Cliente**: Si tiene menos de 3.5 estrellas → ❌ Rechazado (cliente tóxico)

### Filtros con IA (Score 0-100):
3. **Score de Viabilidad**:
   - **80-100**: ✅ Aceptado (automatización, scripts, scraping, webs simples)
   - **65-79**: ✅ Aceptado (proyectos viables)
   - **0-64**: ❌ Rechazado (tareas creativas, hardware, sin sentido)

### Datos que analiza la IA:
- **Título del proyecto**
- **Descripción completa**
- **Presupuesto del cliente**
- **Número de propuestas existentes**
- **Tipo de trabajo** (automatizable vs creativo)

---

## 2. Opinión sobre tu Estrategia

### ✅ **Fortalezas:**
1. **Enfoque agresivo pero inteligente**: "Factura ahora, aprende después" es perfecto para maximizar ingresos
2. **Uso de IA para acelerar**: Muy inteligente usar IAs de código para ser más rápido
3. **Filtrado inteligente**: Evitar clientes tóxicos y proyectos ya procesados
4. **Precios dinámicos**: Usar insight de competencia (70%) es competitivo

### ⚠️ **Mejoras Sugeridas:**

1. **Límite de propuestas diarias (7)**: 
   - ✅ Bueno para evitar spam
   - 💡 Considera aumentar a 10-15 si tienes tiempo para revisar

2. **Score mínimo (65)**:
   - ✅ Conservador y seguro
   - 💡 Podrías bajar a 60 para más oportunidades, o subir a 70 para más calidad

3. **Delays entre propuestas (3-5 min)**:
   - ✅ Bueno para evitar detección
   - 💡 Considera aumentar a 5-10 min para ser más seguro

4. **Falta de logging**:
   - 💡 Agregar logs de qué proyectos aceptó/rechazó y por qué
   - 💡 Estadísticas de éxito (cuántas propuestas → cuántas aceptadas)

5. **No hay rotación de propuestas**:
   - 💡 Considera variar el estilo de propuestas para no parecer repetitivo

6. **Falta validación de presupuesto**:
   - 💡 Rechazar proyectos con presupuesto muy bajo (<$50)

---

## 3. Ejecutar en Segundo Plano (Gratis)

### ❌ **Sin PC prendida - NO es posible gratis**
Para ejecutar sin tener la PC prendida necesitas un servidor, y eso cuesta dinero.

### ✅ **Opciones Gratis (con PC prendida):**

1. **Windows Task Scheduler** (Recomendado):
   ```powershell
   # Crear tarea programada que ejecute el bot cada X horas
   # Busca "Programador de tareas" en Windows
   ```
   - ✅ Gratis
   - ✅ Se ejecuta en segundo plano
   - ⚠️ Necesitas PC prendida

2. **Ejecutar como servicio de Windows**:
   - ✅ Corre en segundo plano siempre
   - ⚠️ Más complejo de configurar

3. **Python con `nohup` o `screen`** (Linux/Mac):
   - ✅ Corre en segundo plano
   - ⚠️ No aplica en Windows

### 💰 **Opciones de Pago (sin PC prendida):**

1. **VPS Gratis (trial)**:
   - Google Cloud (Free Tier)
   - AWS Free Tier
   - Oracle Cloud (siempre gratis)
   - ⚠️ Limitado en recursos

2. **Servicios de hosting**:
   - Railway.app (tier gratis limitado)
   - Render.com (tier gratis)
   - ⚠️ Pueden suspender si detectan bots

### ⚠️ **ADVERTENCIA IMPORTANTE:**
Ejecutar bots automatizados puede violar los Términos de Servicio de Workana. Usa con precaución y considera:
- Ejecutar solo algunas horas al día
- No ser demasiado agresivo
- Revisar manualmente las propuestas antes de enviar

---

## 📈 Recomendaciones Finales

1. **Mantén el enfoque agresivo** pero sé inteligente
2. **Agrega logging** para aprender qué funciona
3. **Revisa manualmente** las primeras propuestas para ajustar
4. **No abuses** - Workana puede detectar patrones
5. **Considera ejecutar solo 2-3 veces al día** en lugar de continuo
