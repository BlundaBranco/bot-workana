"""
Bot automatizado para Workana.

Este módulo contiene la lógica principal del bot:
- Navegación y scraping de proyectos
- Envío de propuestas
- Manejo de sesión y cookies
- Simulación de comportamiento humano
"""

import time
import random
import pickle
import os
import json
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc

from .config import Config
from .ai_assistant import AIAssistant


class WorkanaBot:
    """
    Bot automatizado para buscar y enviar propuestas en Workana.
    
    Características:
    - Login automático con cookies persistentes
    - Scraping inteligente de proyectos
    - Filtrado por historial y rating de clientes
    - Envío de propuestas con comportamiento humano
    - Anti-detección avanzado
    """
    
    def __init__(self):
        """Inicializa el bot con configuración anti-detección."""
        options = uc.ChromeOptions()
        
        # 🛡️ CONFIGURACIÓN ANTI-DETECCIÓN
        user_data_dir = os.path.join(os.getcwd(), "chrome_profile")
        options.add_argument(f'--user-data-dir={user_data_dir}')
        options.add_argument('--profile-directory=Default')
        
        # Modo headless para VPS (sin interfaz gráfica)
        if Config.HEADLESS_MODE:
            options.add_argument('--headless=new')
            options.add_argument('--disable-gpu')
            print("🖥️ Modo headless activado (VPS)")
        else:
            options.add_argument('--start-maximized')
        
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
        options.add_argument('--lang=es-ES,es')
        options.add_argument('--accept-lang=es-ES,es;q=0.9')
        options.add_argument('--window-size=1920,1080')  # Tamaño fijo para headless
        
        # Preferencias de usuario
        prefs = {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "profile.default_content_setting_values.notifications": 2
        }
        options.add_experimental_option("prefs", prefs)
        
        # Inicializar Chrome (sin useAutomationExtension que causa error)
        try:
            self.driver = uc.Chrome(options=options, version_main=None, use_subprocess=True)
        except Exception as e:
            print(f"⚠️ Error con configuración avanzada, intentando básica: {e}")
            # Fallback: configuración mínima pero que funcione en VPS
            options = uc.ChromeOptions()
            
            # Mantener headless si estaba activado
            if Config.HEADLESS_MODE:
                options.add_argument('--headless=new')
                options.add_argument('--disable-gpu')
                options.add_argument('--window-size=1920,1080')
                print("   🖥️ Fallback en modo headless")
            else:
                options.add_argument('--start-maximized')
            
            # Opciones críticas para VPS
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-blink-features=AutomationControlled')
            
            self.driver = uc.Chrome(options=options, version_main=None, use_subprocess=True)
        
        # 🎭 INYECTAR SCRIPTS ANTI-DETECCIÓN
        try:
            self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
                'source': '''
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => undefined
                    });
                    window.navigator.chrome = { runtime: {} };
                    Object.defineProperty(navigator, 'plugins', {
                        get: () => [1, 2, 3, 4, 5]
                    });
                    Object.defineProperty(navigator, 'languages', {
                        get: () => ['es-ES', 'es', 'en']
                    });
                '''
            })
        except Exception as e:
            print(f"⚠️ No se pudieron inyectar scripts anti-detección: {e}")
        
        self.wait = WebDriverWait(self.driver, 15)
        self.ai = AIAssistant(Config.GEMINI_API_KEY)
        self.history = self.load_history()

    def load_history(self):
        """
        Carga el historial de proyectos ya procesados.
        
        Returns:
            Lista de URLs de proyectos ya procesados
        """
        # Asegurar que la carpeta data existe
        os.makedirs(os.path.dirname(Config.HISTORY_FILE), exist_ok=True)
        
        if os.path.exists(Config.HISTORY_FILE):
            try:
                with open(Config.HISTORY_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []

    def save_to_history(self, project_url):
        """
        Guarda un proyecto en el historial para no repetirlo.
        
        Args:
            project_url: URL del proyecto a guardar
        """
        self.history.append(project_url)
        # Asegurar que la carpeta data existe
        os.makedirs(os.path.dirname(Config.HISTORY_FILE), exist_ok=True)
        with open(Config.HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)

    def login(self):
        """
        Maneja el login en Workana.
        
        Prioridad:
        1. Perfil persistente de Chrome (más seguro)
        2. Cookies guardadas
        3. Login manual
        """
        print("🔐 Verificando sesión...")
        self.driver.get(Config.BASE_URL)
        time.sleep(random.uniform(3, 5))
        
        # Verificar si realmente estamos logueados (más estricto)
        # Buscar elementos que solo aparecen cuando estás logueado
        is_logged_in = False
        try:
            # Esperar un poco para que cargue la página
            time.sleep(2)
            page_source = self.driver.page_source.lower()
            current_url = self.driver.current_url.lower()
            
            # Si la URL tiene "login", definitivamente no está logueado
            if "login" in current_url:
                is_logged_in = False
            # Si encuentra elementos típicos de usuario logueado, está logueado
            elif any(indicator in page_source for indicator in ["mi perfil", "dashboard", "propuestas", "mensajes", "notificaciones"]):
                is_logged_in = True
            # Si no hay botón de login visible, probablemente está logueado
            elif "iniciar sesión" not in page_source and "login" not in page_source:
                is_logged_in = True
            else:
                is_logged_in = False
        except:
            is_logged_in = False
        
        if is_logged_in:
            print("✅ Sesión activa detectada (perfil persistente).")
            return
        
        # Intentar cargar cookies
        if os.path.exists(Config.COOKIES_FILE):
            try:
                print("🔑 Intentando cargar cookies guardadas...")
                self.driver.get(Config.BASE_URL)
                print("   📄 Página cargada, esperando...")
                time.sleep(random.uniform(2, 3))
                
                print("   📂 Leyendo archivo de cookies...")
                with open(Config.COOKIES_FILE, 'rb') as f:
                    cookies = pickle.load(f)
                
                print(f"   🍪 Cargando {len(cookies)} cookies...")
                cookies_cargadas = 0
                for c in cookies:
                    try:
                        self.driver.add_cookie(c)
                        cookies_cargadas += 1
                    except Exception as e:
                        pass  # Algunas cookies pueden fallar, continuar
                
                print(f"   ✅ {cookies_cargadas}/{len(cookies)} cookies cargadas")
                print("   🔄 Recargando página...")
                self.driver.refresh()
                time.sleep(random.uniform(4, 6))
                
                print("   🔍 Verificando si el login funcionó...")
                # Verificar nuevamente si está logueado
                page_source = self.driver.page_source.lower()
                current_url = self.driver.current_url.lower()
                
                if "login" not in current_url and any(indicator in page_source for indicator in ["mi perfil", "dashboard", "propuestas"]):
                    print("✅ Login recuperado desde cookies.")
                    return
                else:
                    print("⚠️ Las cookies no funcionaron o expiraron.")
                    print(f"   URL actual: {current_url[:50]}...")
            except Exception as e:
                print(f"⚠️ Error cargando cookies: {e}")
                import traceback
                traceback.print_exc()
        
        # Login manual
        print("⚠️ LOGIN MANUAL REQUERIDO.")
        print("   El navegador se abrirá en la página de login.")
        print("   Por favor, inicia sesión manualmente.")
        self.driver.get(Config.LOGIN_URL)
        time.sleep(random.uniform(*Config.DELAY_PAGE))
        
        if Config.AUTO_MODE:
            print("   ⚠️ MODO AUTO: Esperando 30 segundos para login manual...")
            time.sleep(30)  # Dar tiempo para login manual
        else:
            input("👉 Presiona ENTER SOLO DESPUÉS de haber iniciado sesión completamente...")
        
        # Verificar que realmente se logueó
        time.sleep(2)
        page_source = self.driver.page_source.lower()
        current_url = self.driver.current_url.lower()
        if "login" in current_url:
            print("❌ ERROR: Parece que no se completó el login. Intenta de nuevo.")
            return
        
        try:
            # Asegurar que la carpeta data existe
            os.makedirs(os.path.dirname(Config.COOKIES_FILE), exist_ok=True)
            with open(Config.COOKIES_FILE, 'wb') as f:
                pickle.dump(self.driver.get_cookies(), f)
            print("✅ Cookies guardadas para próxima sesión.")
        except Exception as e:
            print(f"⚠️ Error guardando cookies: {e}")

    def human_scroll(self):
        """Scrollea suavemente para simular lectura humana."""
        try:
            total_height = int(self.driver.execute_script("return document.body.scrollHeight"))
            current = 0
            while current < total_height:
                scroll_amount = random.randint(200, 400)
                current += scroll_amount
                self.driver.execute_script(f"window.scrollTo(0, {current});")
                time.sleep(random.uniform(*Config.DELAY_SCROLL))
            self.driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(random.uniform(*Config.DELAY_SCROLL))
        except:
            pass
    
    def human_type(self, element, text, min_delay=None, max_delay=None):
        """
        Escribe texto simulando velocidad humana con errores ocasionales.
        
        Args:
            element: Elemento de Selenium donde escribir
            text: Texto a escribir
            min_delay: Delay mínimo entre caracteres (usa Config si None)
            max_delay: Delay máximo entre caracteres (usa Config si None)
        """
        element.clear()
        time.sleep(random.uniform(0.2, 0.4))
        
        # Usar delays de Config si no se especifican
        if min_delay is None:
            min_delay = Config.DELAY_TYPE[0]
        if max_delay is None:
            max_delay = Config.DELAY_TYPE[1]
        
        for char in text:
            element.send_keys(char)
            delay = random.uniform(min_delay, max_delay) if len(text) > 50 else random.uniform(min_delay * 1.5, max_delay * 1.5)
            time.sleep(delay)
            
            # Simular error y corrección (5% probabilidad, solo en modo seguro)
            if Config.SPEED_MODE == "safe" and random.random() < 0.05 and len(text) > 10:
                element.send_keys(Keys.BACKSPACE)
                time.sleep(random.uniform(0.1, 0.2))
                element.send_keys(char)
                time.sleep(random.uniform(0.1, 0.2))
    
    def human_click(self, element):
        """
        Hace click de forma más humana con movimiento previo.
        
        Args:
            element: Elemento de Selenium a hacer click
        """
        try:
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", element)
            time.sleep(random.uniform(*Config.DELAY_CLICK))
            try:
                element.click()
            except:
                self.driver.execute_script("arguments[0].click();", element)
            time.sleep(random.uniform(*Config.DELAY_CLICK))
        except Exception as e:
            print(f"      ⚠️ Error en click humano: {e}")
            raise

    def get_smart_price(self, project_url, client_budget_text, bids_count, ai_suggested_price=None):
        """
        Calcula el precio inteligente para la propuesta.
        
        Estrategia:
        - Si hay <5 propuestas: Usa el precio sugerido por la IA
        - Si hay >=5 propuestas: Usa el 70% del insight (precio promedio de competencia)
        - Fallback: Presupuesto promedio del cliente
        
        Args:
            project_url: URL del proyecto
            client_budget_text: Texto del presupuesto del cliente
            bids_count: Número de propuestas existentes
            ai_suggested_price: Precio sugerido por la IA (opcional)
            
        Returns:
            Precio final a ofertar
        """
        # Parsear presupuesto del cliente (fallback)
        client_avg = 50000
        try:
            nums = [int(s) for s in re.findall(r'\d+', client_budget_text.replace('.', ''))]
            if nums:
                client_avg = int(sum(nums) / len(nums))
        except:
            pass

        # Si hay pocas propuestas, usar precio de la IA
        try:
            count = int(bids_count)
            if count < Config.MIN_BIDS_FOR_INSIGHT:
                if ai_suggested_price:
                    print(f"      💰 Pocas propuestas ({count}). Usando precio de IA: ${ai_suggested_price}")
                    return ai_suggested_price
                else:
                    print(f"      ⚠️ Pocas propuestas ({count}) pero sin precio de IA. Usando presupuesto cliente: ${client_avg}")
                    return client_avg
        except:
            pass

        # Si hay muchas propuestas, usar insight (70% del promedio de competencia)
        try:
            insight_url = project_url.replace("/job/", "/job/insight/") if "/insight/" not in project_url else project_url
            print("      🔍 Consultando insight de precios...")
            self.driver.get(insight_url)
            time.sleep(random.uniform(3, 5))
            
            self.driver.execute_script("window.scrollTo(0, 300);")
            time.sleep(random.uniform(1, 2))
            
            selectors = ["div.col-sm-3.text-right span", "#appH4", "h4.abig"]
            for sel in selectors:
                try:
                    elem = self.driver.find_element(By.CSS_SELECTOR, sel)
                    if any(c.isdigit() for c in elem.text):
                        raw = int(re.sub(r'[^\d]', '', elem.text))
                        final_price = int(raw * Config.PRICE_PERCENTAGE)
                        print(f"      💰 Insight detectado: ${raw} → Oferta: ${final_price} (70%)")
                        return final_price
                except:
                    continue
        except Exception as e:
            print(f"      ⚠️ No se pudo obtener insight: {e}")
        
        # Fallback: presupuesto del cliente
        return client_avg

    def fill_and_send_proposal(self, project_url, price, days, text):
        """
        Llena y envía una propuesta en Workana.
        
        Args:
            project_url: URL del proyecto
            price: Precio a ofertar
            days: Días de entrega
            text: Texto de la propuesta
            
        Returns:
            True si se envió exitosamente, False en caso contrario
        """
        try:
            clean_url = project_url.replace("/job/insight/", "/job/")
            print(f"   🚀 Yendo a ofertar: {clean_url}")
            
            self.driver.get(clean_url)
            time.sleep(random.uniform(*Config.DELAY_PAGE))
            
            # Verificar sesión
            if "login" in self.driver.current_url.lower():
                print("      ❌ Sesión expirada. Reloguea y reinicia el bot.")
                return False
            
            # Simular lectura
            print("      👀 Simulando lectura del proyecto...")
            self.human_scroll()
            time.sleep(random.uniform(*Config.DELAY_PAGE))
            
            try:
                bid_btn = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#bid_button")))
                
                # Verificar si ya ofertaste
                if "ya has enviado" in self.driver.page_source.lower() or "already sent" in self.driver.page_source.lower():
                    print("      ⚠️ Ya enviaste propuesta a este proyecto.")
                    self.save_to_history(clean_url)
                    return False
                
                print("      🖱️ Haciendo click en 'Ofertar'...")
                self.human_click(bid_btn)
                time.sleep(random.uniform(*Config.DELAY_PAGE))
                
            except Exception as e:
                print(f"      ❌ No encontré botón 'Ofertar': {e}")
                return False
                
            print("      📝 Llenando formulario (simulando escritura humana)...")
            time.sleep(random.uniform(*Config.DELAY_PAGE))
            
            # PRECIO
            try:
                amount_in = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#Amount")))
                amount_in.click()
                time.sleep(random.uniform(*Config.DELAY_CLICK))
                self.human_type(amount_in, str(price))
                time.sleep(random.uniform(*Config.DELAY_CLICK))
            except Exception as e:
                print(f"      ⚠️ Error llenando precio: {e}")
                return False
            
            # TIEMPO
            try:
                time_in = self.driver.find_element(By.CSS_SELECTOR, "#BidDeliveryTime")
                time_in.click()
                time.sleep(random.uniform(*Config.DELAY_CLICK))
                time_text = f"{days} Días"
                self.human_type(time_in, time_text)
                time.sleep(random.uniform(*Config.DELAY_CLICK))
            except Exception as e:
                print(f"      ⚠️ Error llenando tiempo: {e}")
                return False
            
            # TEXTO
            try:
                text_area = self.driver.find_element(By.CSS_SELECTOR, "#BidContent")
                text_area.click()
                time.sleep(random.uniform(0.5, 1.0))
                print("      ⌨️ Escribiendo propuesta (esto puede tardar un momento)...")
                self.human_type(text_area, text, min_delay=0.03, max_delay=0.08)
                time.sleep(random.uniform(1, 2))
            except Exception as e:
                print(f"      ⚠️ Error llenando texto: {e}")
                return False
            
            # SKILLS
            try:
                skills = self.driver.find_elements(By.CSS_SELECTOR, "div.display-selector label")
                count = 0
                for skill in skills:
                    if count >= 5:
                        break
                    self.human_click(skill)
                    count += 1
                    time.sleep(random.uniform(*Config.DELAY_CLICK))
            except:
                pass

            # PORTFOLIO
            try:
                portfolio_btns = self.driver.find_elements(By.CSS_SELECTOR, "#selectPortfolio")
                count = 0
                for btn in portfolio_btns:
                    if count >= 3:
                        break
                    if btn.is_displayed():
                        self.human_click(btn)
                        count += 1
                        time.sleep(random.uniform(*Config.DELAY_CLICK))
            except:
                pass

            # EXTRAS - Limpiar tareas de la propuesta (selector mejorado)
            print("      🧹 Limpiando tareas extras...")
            # Buscar todos los botones de eliminar tareas (más robusto)
            # El selector puede variar, así que buscamos por múltiples patrones
            selectors_to_try = [
                "#bidForm > div.row > div.col-md-9 > div:nth-child(5) > div > section > div:nth-child(1) > div > button",
                "#bidForm button[type='button']",  # Botones genéricos
                "section button",  # Cualquier botón en secciones
            ]
            
            max_tries = 15  # Más intentos por si hay muchas tareas
            deleted_count = 0
            
            while max_tries > 0:
                found_any = False
                for selector in selectors_to_try:
                    try:
                        # Buscar todos los botones que coincidan
                        buttons = self.driver.find_elements(By.CSS_SELECTOR, selector)
                        for btn in buttons:
                            try:
                                # Verificar que el botón sea visible y tenga un ícono de cerrar
                                if btn.is_displayed():
                                    btn_html = btn.get_attribute('outerHTML')
                                    # Si tiene un ícono "x" o "close" o está en una sección de tareas
                                    if 'i' in btn_html.lower() or btn.find_elements(By.TAG_NAME, 'i'):
                                        self.human_click(btn)
                                        time.sleep(random.uniform(0.5, 1.0))
                                        deleted_count += 1
                                        found_any = True
                                        break  # Solo uno a la vez
                            except:
                                continue
                        if found_any:
                            break
                    except:
                        continue
                
                if not found_any:
                    # Si no encuentra más, salir
                    break
                
                max_tries -= 1
                time.sleep(random.uniform(0.3, 0.5))
            
            if deleted_count > 0:
                print(f"      ✅ Eliminadas {deleted_count} tareas extras.")
            else:
                print("      ℹ️ No se encontraron tareas extras para eliminar.")

            # Pausa final
            print("      ⏸️ Pausa final antes de enviar...")
            time.sleep(random.uniform(*Config.DELAY_PAGE))

            # ENVIAR
            submit_selector = "#bidForm > div.row > div.col-md-9 > div.wk-submit-block > input"
            submit_btn = self.driver.find_element(By.CSS_SELECTOR, submit_selector)
            
            print("\n" + "="*50)
            print(f"      💵 Oferta: ${price} | ⏱️ {time_text}")
            print("      👀 PROPUESTA GENERADA (Fragmento):")
            print(f"      {text[:150]}...")
            print("="*50)
            
            if Config.AUTO_MODE:
                print("      🤖 MODO AUTO: Enviando automáticamente en 3 segundos...")
                time.sleep(3)
            else:
                input("      🔴 Presiona ENTER para ENVIAR la propuesta (revisa que todo esté OK)...")
            
            print("      📤 Enviando propuesta...")
            self.human_click(submit_btn)
            time.sleep(random.uniform(4, 6))
            
            # Verificar resultado
            page_source_lower = self.driver.page_source.lower()
            current_url_lower = self.driver.current_url.lower()
            
            if "forbidden" in page_source_lower or "forbidden" in current_url_lower:
                print("      ❌ ERROR: Workana rechazó la propuesta (Forbidden)")
                print(f"      🔍 URL actual: {self.driver.current_url}")
                print("      💡 CAUSA PROBABLE: Detección de bot. Revisa cookies y espera antes de reintentar.")
                return False
            
            if "gracias" in page_source_lower or "enviada" in page_source_lower or "success" in page_source_lower:
                print("      🎉 ¡PROPUESTA ENVIADA CON ÉXITO!")
            else:
                print("      ⚠️ Estado incierto. Revisa manualmente si se envió.")
            
            self.save_to_history(clean_url)
            return True

        except Exception as e:
            print(f"      ❌ Error llenando formulario: {e}")
            import traceback
            traceback.print_exc()
            return False

    def run(self):
        """
        Ejecuta el ciclo principal del bot.
        
        Flujo:
        1. Login
        2. Scraping de proyectos
        3. Filtrado (historial, rating)
        4. Análisis con IA
        5. Envío de propuestas
        """
        try:
            self.login()
            print("🔍 Escaneando proyectos...")
            self.driver.get(Config.SEARCH_URL)
            time.sleep(random.uniform(3, 5))
            
            try:
                self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.project-item")))
                time.sleep(random.uniform(1, 2))
            except:
                print("⚠️ No cargaron los proyectos.")
                return

            # Extraer proyectos
            cards = self.driver.find_elements(By.CSS_SELECTOR, "div.project-item.js-project")
            
            candidates_raw = []
            for card in cards:
                try:
                    data = self.driver.execute_script("""
                        var card = arguments[0];
                        var title_el = card.querySelector('h2.project-title > span > a');
                        var budget_el = card.querySelector('span.budget') || card.querySelector('span.values');
                        var bids_el = card.querySelector('span.bids');
                        var date_el = card.querySelector('span.date');
                        var desc_el = card.querySelector('div.html-desc');
                        var stars_el = card.querySelector('span.stars-rating');
                        
                        return {
                            title: title_el ? (title_el.getAttribute('title') || title_el.textContent.trim()) : null,
                            url: title_el ? title_el.href : null,
                            budget_text: budget_el ? budget_el.textContent.trim() : 'N/A',
                            bids_count: bids_el ? bids_el.textContent.trim() : '0',
                            date_text: date_el ? date_el.textContent.trim() : 'N/A',
                            description: desc_el ? desc_el.textContent.trim() : 'Sin descripción previa',
                            stars_class: stars_el ? stars_el.className : null
                        };
                    """, card)
                    
                    if data and data['url']:
                        candidates_raw.append(data)
                        
                except Exception as e:
                    print(f"⚠️ Error extrayendo tarjeta: {e}")
                    continue
            
            scan_limit = 20
            candidates_raw = candidates_raw[:scan_limit]
            print(f"📊 {len(candidates_raw)} tarjetas extraídas. Filtrando...")
            
            # Filtrar
            candidates = []
            for p in candidates_raw:
                # Filtro de historial
                if p['url'] in self.history:
                    print(f"   ⏭️ Saltando proyecto ya procesado: {p['title'][:30]}...")
                    continue
                
                # Filtro de rating
                if p['stars_class']:
                    rating_match = re.search(r'stars-(\d+)', p['stars_class'])
                    if rating_match:
                        rating = int(rating_match.group(1))
                        if rating < 35:
                            print(f"   💀 Cliente tóxico detectado (Rating {rating/10}). Saltando.")
                            continue
                
                p['bids_count'] = re.sub(r'[^\d]', '', p['bids_count']) or '0'
                candidates.append(p)
            
            print(f"🧠 {len(candidates)} Proyectos nuevos y viables. Filtrando con IA...")

            sent_count = 0
            for p in candidates:
                # Limitar por ejecución para distribuir mejor (52/semana = 2 ejecuciones/día de 5-6)
                if sent_count >= Config.MAX_PROPOSALS_PER_EXECUTION:
                    print(f"🛑 Límite por ejecución alcanzado ({Config.MAX_PROPOSALS_PER_EXECUTION} propuestas).")
                    break
                
                # También verificar límite diario
                if sent_count >= Config.MAX_PROPOSALS_PER_DAY:
                    print("🛑 Límite diario alcanzado (7 propuestas).")
                    break

                print(f"\n🔹 {p['title'][:40]}... | 🕒 {p['date_text']} | 👥 {p['bids_count']} bids")
                
                # Análisis con IA
                analysis = self.ai.analyze_project(p)
                
                if not analysis:
                    print("   ⚠️ La IA no respondió. Saltando.")
                    continue
                
                if analysis['score'] < Config.MIN_SCORE_TO_BID:
                    self.save_to_history(p['url'])
                    print(f"   ❌ RECHAZADO (Score: {analysis['score']}) | {analysis.get('reason','')}")
                    continue
                
                print(f"   ✅ ACEPTADO (Score: {analysis['score']}).")
                
                # Calcular precio (usa precio de IA si hay pocas propuestas)
                ai_price = analysis.get('suggested_price')
                final_price = self.get_smart_price(
                    p['url'], 
                    p['budget_text'], 
                    p['bids_count'],
                    ai_suggested_price=ai_price
                )
                
                success = self.fill_and_send_proposal(
                    p['url'], 
                    final_price, 
                    analysis['delivery_days'], 
                    analysis['proposal_text']
                )
                
                if success:
                    sent_count += 1
                    wait_time = random.randint(*Config.DELAY_BETWEEN_PROPOSALS)
                    print(f"⏳ Esperando {wait_time//60} minutos antes de la siguiente propuesta...")
                    time.sleep(wait_time)
                    
                    # Verificar sesión
                    try:
                        self.driver.get(Config.BASE_URL)
                        time.sleep(2)
                        if "login" in self.driver.current_url.lower():
                            print("⚠️ Sesión expirada. Deteniendo bot.")
                            break
                    except:
                        pass

        except Exception as e:
            print(f"❌ Error fatal en ejecución: {e}")
            import traceback
            traceback.print_exc()
        finally:
            if self.driver:
                print("👋 Cerrando navegador.")
                self.driver.quit()
