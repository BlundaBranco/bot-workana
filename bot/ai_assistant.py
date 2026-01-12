"""
Asistente de IA para análisis de proyectos y generación de propuestas.

Este módulo maneja toda la interacción con la API de Gemini para:
- Analizar proyectos y determinar si son viables
- Generar propuestas personalizadas
- Calcular precios y tiempos de entrega agresivos pero realistas
"""

import time
import json
import re
import google.generativeai as genai


class AIAssistant:
    """
    Asistente de IA que analiza proyectos y genera propuestas.
    
    La IA sabe que eres un programador experto que usa las últimas IAs
    para generar código, permitiendo precios y tiempos agresivos.
    """
    
    def __init__(self, api_key):
        """
        Inicializa el asistente de IA.
        
        Args:
            api_key: Clave de API de Gemini
            
        Raises:
            ValueError: Si falta la API key
        """
        if not api_key:
            raise ValueError("❌ FALTA GEMINI_KEY")
        genai.configure(api_key=api_key)

    def analyze_project(self, project_data):
        """
        Analiza un proyecto y genera una propuesta completa.
        
        La IA sabe que:
        - Eres experto en TODO (especialmente en el trabajo específico)
        - Usas las últimas IAs para generar código (pero NO lo menciona)
        - Debes ser agresivo en precio/tiempo pero realista
        - Regla: "Factura ahora, aprende después"
        
        Args:
            project_data: Diccionario con datos del proyecto:
                - title: Título del proyecto
                - description: Descripción completa
                - budget_text: Presupuesto del cliente
                - bids_count: Número de propuestas existentes
                
        Returns:
            Dict con:
                - is_relevant: bool
                - score: int (0-100)
                - reason: str
                - delivery_days: int
                - proposal_text: str
                - suggested_price: int (precio sugerido por la IA)
            None si hay error
        """
        prompt = f"""
        ACTÚA COMO: Un Ingeniero de Software Senior con 10 años de experiencia.
        TONO: Seco, directo, profesional. CERO entusiasmo artificial.
        OBJETIVO: Identificar si es un proyecto automatizable y ganar la oferta.

        CONTEXTO CRÍTICO (NO MENCIONAR AL CLIENTE):
        - Eres experto en TODO, especialmente en este trabajo específico.
        - Usas las últimas IAs de generación de código (Claude, GPT-4, Cursor, etc.) que son una locura.
        - Esto te permite ser MUY rápido y eficiente.
        - REGLA: "Factura ahora, aprende después" - Acepta proyectos que puedas resolver con IA.
        - Debes ser AGRESIVO en precio y tiempo, pero realista (no imposible).

        DATOS DEL PROYECTO:
        Título: {project_data['title']}
        Descripción: {project_data['description']}
        Presupuesto Cliente: {project_data['budget_text']}
        Competencia: {project_data['bids_count']} propuestas.

        INSTRUCCIONES CRÍTICAS (ANTI-BOT):
        1. **DETECTOR DE TRAMPAS:** Busca en la descripción si el cliente pide escribir una palabra específica al inicio (ej: "Escribe 'hola' al empezar"). Si existe, LA PRIMERA PALABRA DE TU PROPUESTA DEBE SER ESA.
        2. **PERSONALIZACIÓN:** Menciona un detalle técnico específico de la descripción para demostrar que leíste.
        3. **SCORE DE VIABILIDAD (0-100):** 
           - 80-100: Tareas de automatización, scripts, scraping, webs simples (Dinero fácil con IA).
           - 0-40: Tareas creativas subjetivas, hardware, o descripciones sin sentido.

        ESTRATEGIA DE VENTA (CAMALEÓN):
        - **JAMÁS menciones IA.** Tu rapidez es por "módulos propios", "experiencia" o "metodología optimizada".
        - Si hay mucha competencia (>20), sé más agresivo en el precio/tiempo.
        - Si hay pocas propuestas (<5), puedes ser más agresivo porque hay menos competencia.
        
        PRECIO Y TIEMPO (AGRESIVOS PERO REALISTAS):
        - Considera que puedes usar IAs para acelerar el desarrollo.
        - El precio debe ser competitivo pero no regalado (30-50% del presupuesto del cliente si hay pocas propuestas).
        - El tiempo debe ser 2-3x más rápido que un desarrollador tradicional (pero no imposible).
        - Ejemplo: Si un proyecto normalmente toma 7 días, ofrécelo en 2-3 días.
        - Ejemplo: Si el presupuesto es $1000, ofrécelo en $400-600 si hay pocas propuestas.
        
        REDACCIÓN (HUMANA):
        - PROHIBIDO usar: "Hola", "Espero que estés bien", "Estoy emocionado", "¡!".
        - Estilo Senior: "Leí tu requerimiento sobre [X]. Puedo resolverlo implementando [Y]."
        - Cierre: "¿Tienes la documentación lista?" o similar.

        OUTPUT JSON:
        {{
            "is_relevant": true,
            "score": (0-100),
            "reason": "...",
            "delivery_days": (entero, tiempo agresivo pero realista),
            "proposal_text": "Texto plano...",
            "suggested_price": (entero, precio agresivo pero competitivo)
        }}
        """
        
        # Lista de modelos a probar (de más rápido a más potente)
        modelos = [
            'models/gemini-2.5-flash-lite',
            'models/gemini-2.0-flash-lite', 
            'models/gemini-2.5-flash',
            'models/gemini-2.0-flash',
            'models/gemini-flash-latest',
            'models/gemini-2.5-pro'
        ]
        
        for m in modelos:
            try:
                model = genai.GenerativeModel(m)
                time.sleep(1)  # Rate limiting
                res = model.generate_content(prompt)
                if not res.text:
                    continue
                # Limpiar formato JSON
                text = re.sub(r'```json|```', '', res.text.strip())
                return json.loads(text)
            except Exception as e:
                error_msg = str(e)
                # Mostrar solo el primer error con detalle para debug
                if m == modelos[0]:
                    print(f"      ⚠️ Error con {m}: {error_msg[:200]}")
                continue
        
        print("      ❌ Error: La IA no pudo generar respuesta. Verifica GEMINI_KEY en .env")
        return None
