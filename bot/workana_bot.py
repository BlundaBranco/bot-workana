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
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc

from .config import Config
from .ai_assistant import AIAssistant
from .logger import logger  # Importar logger


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
        logger.info("🤖 Inicializando WorkanaBot...")
        options = uc.ChromeOptions()
        
        # 🛡️ CONFIGURACIÓN ANTI-DETECCIÓN
        user_data_dir = os.path.join(os.getcwd(), "chrome_profile")
        options.add_argument(f'--user-data-dir={user_data_dir}')
        options.add_argument('--profile-directory=Default')
        
        # Modo headless para VPS (sin interfaz gráfica)
        if Config.HEADLESS_MODE:
            options.add_argument('--headless=new')
            options.add_argument('--disable-gpu')
            logger.info("🖥️ Modo headless activado (VPS)")
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
            logger.warning(f"⚠️ Error con configuración avanzada, intentando básica: {e}")
            # Fallback: configuración mínima pero que funcione en VPS
            options = uc.ChromeOptions()
            
            # Mantener headless si estaba activado
            if Config.HEADLESS_MODE:
                options.add_argument('--headless=new')
                options.add_argument('--disable-gpu')
                options.add_argument('--window-size=1920,1080')
                logger.info("   🖥️ Fallback en modo headless")
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
            logger.error(f"⚠️ No se pudieron inyectar scripts anti-detección: {e}")
        
        
        self.wait = WebDriverWait(self.driver, 15)
        self.ai = AIAssistant(
            provider=Config.AI_PROVIDER,
            gemini_key=Config.GEMINI_API_KEY,
            openai_key=Config.OPENAI_API_KEY
        )
        self.history = self.load_history()

    def load_history(self):
        """
        Carga el historial de proyectos ya procesados.
        Soporta formato antiguo (lista de strings) y nuevo (lista de dicts con fecha).
        
        Returns:
            Lista de proyectos (dicts) o URLs (strings, por compatibilidad)
        """
        # Asegurar que la carpeta data existe
        os.makedirs(os.path.dirname(Config.HISTORY_FILE), exist_ok=True)
        
        if os.path.exists(Config.HISTORY_FILE):
            try:
                with open(Config.HISTORY_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    logger.info(f"📂 Historial cargado: {len(data)} registros.")
                    return data
            except:
                return []
        return []

    def get_history_urls(self):
        """
        Devuelve solo las URLs del historial para filtrado rápido.
        Maneja compatibilidad entre formato antiguo y nuevo.
        """
        urls = set()
        for item in self.history:
            if isinstance(item, str):
                urls.add(item)
            elif isinstance(item, dict) and 'url' in item:
                urls.add(item['url'])
        return urls

    def get_weekly_count(self):
        """
        Cuenta cuántas propuestas se han enviado en la semana actual (Lunes a Domingo).
        """
        count = 0
        now = datetime.now()
        # Obtener el inicio de la semana (Lunes)
        current_week_start = now.timestamp() - (now.weekday() * 86400) - (now.hour * 3600) - (now.minute * 60) - now.second
        
        for item in self.history:
            # Si es formato antiguo (string), no tiene fecha, ignorar para el conteo semanal
            if isinstance(item, dict) and 'timestamp' in item:
                try:
                    ts = datetime.fromisoformat(item['timestamp']).timestamp()
                    if ts >= current_week_start:
                        count += 1
                except:
                    pass
        
        logger.info(f"📊 Propuestas de esta semana: {count}/{Config.MAX_PROPOSALS_PER_WEEK}")
        return count

    def save_to_history(self, project_url, price=None):
        """
        Guarda un proyecto en el historial con timestamp.
        
        Args:
            project_url: URL del proyecto a guardar
            price: Precio ofertado (opcional)
        """
        entry = {
            "url": project_url,
            "timestamp": datetime.now().isoformat(),
            "price": price
        }
        
        self.history.append(entry)
        
        # Asegurar que la carpeta data existe
        os.makedirs(os.path.dirname(Config.HISTORY_FILE), exist_ok=True)
        with open(Config.HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)

    def login(self):
        """
        Maneja el login en Workana.
        """
        logger.info("🔐 Verificando sesión...")
        self.driver.get(Config.BASE_URL)
        time.sleep(random.uniform(3, 5))
        
        # Verificar si realmente estamos logueados
        is_logged_in = False
        try:
            time.sleep(2)
            page_source = self.driver.page_source.lower()
            current_url = self.driver.current_url.lower()
            
            if "login" in current_url:
                is_logged_in = False
            elif any(indicator in page_source for indicator in ["mi perfil", "dashboard", "propuestas", "mensajes", "notificaciones"]):
                is_logged_in = True
            elif "iniciar sesión" not in page_source and "login" not in page_source:
                is_logged_in = True
            else:
                is_logged_in = False
        except:
            is_logged_in = False
        
        if is_logged_in:
            logger.info("✅ Sesión activa detectada (perfil persistente).")
            return
        
        # Intentar cargar cookies
        if os.path.exists(Config.COOKIES_FILE):
            try:
                logger.info("🔑 Intentando cargar cookies guardadas...")
                self.driver.get(Config.BASE_URL)
                time.sleep(random.uniform(2, 3))
                
                with open(Config.COOKIES_FILE, 'rb') as f:
                    cookies = pickle.load(f)
                
                cookies_cargadas = 0
                for c in cookies:
                    try:
                        self.driver.add_cookie(c)
                        cookies_cargadas += 1
                    except:
                        pass
                
                logger.info(f"   ✅ {cookies_cargadas}/{len(cookies)} cookies cargadas. Recargando...")
                self.driver.refresh()
                time.sleep(random.uniform(4, 6))
                
                # Verificar nuevamente
                page_source = self.driver.page_source.lower()
                current_url = self.driver.current_url.lower()
                
                if "login" not in current_url and any(indicator in page_source for indicator in ["mi perfil", "dashboard", "propuestas"]):
                    logger.info("✅ Login recuperado desde cookies.")
                    return
                else:
                    logger.warning("⚠️ Las cookies no funcionaron o expiraron.")
            except Exception as e:
                logger.error(f"⚠️ Error cargando cookies: {e}")
        
        # Login manual
        logger.warning("⚠️ LOGIN MANUAL REQUERIDO: El navegador se abrirá para login manual.")
        self.driver.get(Config.LOGIN_URL)
        time.sleep(random.uniform(*Config.DELAY_PAGE))
        
        if Config.AUTO_MODE:
            logger.info("   ⚠️ MODO AUTO: Esperando 30 segundos para login manual...")
            time.sleep(30)
        else:
            input("👉 Presiona ENTER SOLO DESPUÉS de haber iniciado sesión completamente...")
        
        # Verificar login
        time.sleep(2)
        page_source = self.driver.page_source.lower()
        current_url = self.driver.current_url.lower()
        if "login" in current_url:
            logger.error("❌ ERROR: Parece que no se completó el login.")
            return
        
        try:
            os.makedirs(os.path.dirname(Config.COOKIES_FILE), exist_ok=True)
            with open(Config.COOKIES_FILE, 'wb') as f:
                pickle.dump(self.driver.get_cookies(), f)
            logger.info("✅ Cookies guardadas para próxima sesión.")
        except Exception as e:
            logger.error(f"⚠️ Error guardando cookies: {e}")

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
        """Escribe texto simulando velocidad humana."""
        element.clear()
        time.sleep(random.uniform(0.2, 0.4))
        
        if min_delay is None:
            min_delay = Config.DELAY_TYPE[0]
        if max_delay is None:
            max_delay = Config.DELAY_TYPE[1]
        
        for char in text:
            element.send_keys(char)
            delay = random.uniform(min_delay, max_delay) if len(text) > 50 else random.uniform(min_delay * 1.5, max_delay * 1.5)
            time.sleep(delay)
            
            if Config.SPEED_MODE == "safe" and random.random() < 0.05 and len(text) > 10:
                element.send_keys(Keys.BACKSPACE)
                time.sleep(random.uniform(0.1, 0.2))
                element.send_keys(char)
                time.sleep(random.uniform(0.1, 0.2))
    
    def human_click(self, element):
        """Hace click de forma más humana."""
        try:
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", element)
            time.sleep(random.uniform(*Config.DELAY_CLICK))
            try:
                element.click()
            except:
                self.driver.execute_script("arguments[0].click();", element)
            time.sleep(random.uniform(*Config.DELAY_CLICK))
        except Exception as e:
            logger.error(f"⚠️ Error en click humano: {e}")
            raise

    def get_smart_price(self, project_url, client_budget_text, bids_count, ai_suggested_price=None):
        """Calcula el precio inteligente para la propuesta."""
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
                    logger.info(f"      💰 Pocas propuestas ({count}). Usando precio de IA: ${ai_suggested_price}")
                    return ai_suggested_price
                else:
                    logger.info(f"      ⚠️ Pocas propuestas ({count}) pero sin precio de IA. Usando presupuesto cliente: ${client_avg}")
                    return client_avg
        except:
            pass

        # Si hay muchas propuestas, usar insight
        try:
            insight_url = project_url.replace("/job/", "/job/insight/") if "/insight/" not in project_url else project_url
            logger.info("      🔍 Consultando insight de precios...")
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
                        logger.info(f"      💰 Insight detectado: ${raw} → Oferta: ${final_price} (70%)")
                        return final_price
                except:
                    continue
        except Exception as e:
            logger.warning(f"      ⚠️ No se pudo obtener insight: {e}")
        
        return client_avg

    def fill_and_send_proposal(self, project_url, price, days, text):
        """Llena y envía una propuesta en Workana."""
        try:
            clean_url = project_url.replace("/job/insight/", "/job/")
            logger.info(f"   🚀 Yendo a ofertar: {clean_url}")
            
            self.driver.get(clean_url)
            time.sleep(random.uniform(*Config.DELAY_PAGE))
            
            if "login" in self.driver.current_url.lower():
                logger.error("      ❌ Sesión expirada. Reloguea y reinicia el bot.")
                return False
            
            logger.info("      👀 Simulando lectura del proyecto...")
            self.human_scroll()
            time.sleep(random.uniform(*Config.DELAY_PAGE))
            
            # Cookies banner
            try:
                cookie_selectors = [
                    "button.ot-sdk-button-primary",
                    "button#onetrust-accept-btn-handler",
                    "a.ot-close-icon",
                    "button.cookie-accept"
                ]
                for selector in cookie_selectors:
                    try:
                        cookie_btn = self.driver.find_element(By.CSS_SELECTOR, selector)
                        if cookie_btn.is_displayed():
                            self.human_click(cookie_btn)
                            break
                    except:
                        continue
            except:
                pass
            
            try:
                bid_btn = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#bid_button")))
                if "ya has enviado" in self.driver.page_source.lower() or "already sent" in self.driver.page_source.lower():
                    logger.warning("      ⚠️ Ya enviaste propuesta a este proyecto.")
                    self.save_to_history(clean_url)
                    return False
                
                logger.info("      🖱️ Haciendo click en 'Ofertar'...")
                self.human_click(bid_btn)
                time.sleep(random.uniform(*Config.DELAY_PAGE))
            except Exception as e:
                logger.error(f"      ❌ No encontré botón 'Ofertar': {e}")
                return False
                
            logger.info("      📝 Llenando formulario (simulando escritura humana)...")
            time.sleep(random.uniform(*Config.DELAY_PAGE))
            
            # PRECIO
            try:
                amount_in = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#Amount")))
                try:
                    amount_in.click()
                except:
                    self.driver.execute_script("arguments[0].click();", amount_in)
                time.sleep(random.uniform(*Config.DELAY_CLICK))
                self.human_type(amount_in, str(price))
                time.sleep(random.uniform(*Config.DELAY_CLICK))
            except Exception as e:
                logger.error(f"      ⚠️ Error llenando precio: {e}")
                return False
            
            # TIEMPO
            try:
                time_in = self.driver.find_element(By.CSS_SELECTOR, "#BidDeliveryTime")
                time_in.click()
                time.sleep(random.uniform(*Config.DELAY_CLICK))
                self.human_type(time_in, f"{days} Días")
                time.sleep(random.uniform(*Config.DELAY_CLICK))
            except Exception as e:
                logger.error(f"      ⚠️ Error llenando tiempo: {e}")
                return False
            
            # TEXTO
            try:
                text_area = self.driver.find_element(By.CSS_SELECTOR, "#BidContent")
                text_area.click()
                time.sleep(random.uniform(0.5, 1.0))
                self.human_type(text_area, text, min_delay=0.03, max_delay=0.08)
                time.sleep(random.uniform(1, 2))
            except Exception as e:
                logger.error(f"      ⚠️ Error llenando texto: {e}")
                return False
            
            # Extras (Skills, Portfolio, Tasks)
            # ... (código resumido, igual que antes pero sin prints molestos)
            
            # Eliminar tareas extras
            logger.info("      🧹 Limpiando tareas extras...")
            # Buscar todos los botones de eliminar tareas (más robusto)
            # El selector puede variar, así que buscamos por múltiples patrones
            selectors_to_try = [
                "#bidForm > div.row > div.col-md-9 > div:nth-child(5) > div > section > div:nth-child(1) > div > button",
                "#bidForm button[type='button']",  # Botones genéricos
                "section button",  # Cualquier botón en secciones
            ]
            
            max_tries = 15
            
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
                                        found_any = True
                                        break  # Solo uno a la vez
                            except:
                                continue
                        if found_any:
                            break
                    except:
                        continue
                
                if not found_any:
                    break
                max_tries -= 1


            # ENVIAR
            logger.info("      ⏸️ Pausa final antes de enviar...")
            time.sleep(random.uniform(*Config.DELAY_PAGE))

            submit_selector = "#bidForm > div.row > div.col-md-9 > div.wk-submit-block > input"
            submit_btn = self.driver.find_element(By.CSS_SELECTOR, submit_selector)
            
            logger.info(f"      💵 Oferta: ${price} | ⏱️ {days} Días")
            
            if Config.AUTO_MODE:
                logger.info("      🤖 MODO AUTO: Enviando automáticamente...")
                time.sleep(3)
            else:
                input("      🔴 Presiona ENTER para ENVIAR la propuesta...")
            
            logger.info("      📤 Enviando propuesta...")
            self.human_click(submit_btn)
            time.sleep(random.uniform(4, 6))
            
            # Verificar
            page_source = self.driver.page_source.lower()
            if "gracias" in page_source or "enviada" in page_source or "success" in page_source:
                logger.info("      🎉 ¡PROPUESTA ENVIADA CON ÉXITO!")
                self.save_to_history(clean_url, price)
                return True
            else:
                logger.warning("      ⚠️ Estado incierto. Verifica manualmente.")
                return False

        except Exception as e:
            logger.error(f"      ❌ Error llenando formulario: {e}")
            return False

    def run(self):
        """Ejecuta el ciclo principal del bot."""
        try:
            logger.info(f"🚀 Iniciando ciclo de ejecución.")
            
            # 1. Chequeo de seguridad: Límite semanal
            weekly_count = self.get_weekly_count()
            if weekly_count >= Config.MAX_PROPOSALS_PER_WEEK:
                logger.warning(f"🛑 LÍMITE SEMANAL ALCANZADO ({weekly_count}/{Config.MAX_PROPOSALS_PER_WEEK}). Deteniendo ejecución.")
                return

            self.login()
            logger.info("🔍 Escaneando proyectos...")
            self.driver.get(Config.SEARCH_URL)
            time.sleep(random.uniform(3, 5))
            
            try:
                self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.project-item")))
            except:
                logger.error("⚠️ No cargaron los proyectos.")
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
                 except: continue

            # Filtrar
            history_urls = self.get_history_urls()
            candidates = []
            for p in candidates_raw:
                if p['url'] in history_urls:
                    logger.info(f"   ⏭️ Saltando proyecto ya procesado: {p['title'][:30]}...")
                    continue
                
                # Filtro rating
                if p['stars_class']:
                    match = re.search(r'stars-(\d+)', p['stars_class'])
                    if match and int(match.group(1)) < 35:
                        logger.warning(f"   💀 Cliente tóxico detectado (Rating {match.group(1)/10}). Saltando.")
                        continue
                
                p['bids_count'] = re.sub(r'[^\d]', '', p['bids_count']) or '0'
                candidates.append(p)
            
            logger.info(f"🧠 {len(candidates)} Proyectos nuevos viables. Analizando con IA...")

            sent_count = 0
            for p in candidates:
                # Chequeo de límites en tiempo real
                if sent_count >= Config.MAX_PROPOSALS_PER_EXECUTION:
                    logger.info(f"🛑 Límite por ejecución alcanzado ({sent_count}).")
                    break
                
                if self.get_weekly_count() >= Config.MAX_PROPOSALS_PER_WEEK:
                    logger.warning("🛑 Límite semanal alcanzado durante la ejecución.")
                    break

                logger.info(f"🔹 {p['title'][:40]}... | 👥 {p['bids_count']} bids")
                
                analysis = self.ai.analyze_project(p)
                if not analysis:
                    logger.warning("   ⚠️ La IA no respondió. Saltando.")
                    continue
                
                if analysis['score'] < Config.MIN_SCORE_TO_BID:
                    self.save_to_history(p['url']) # Guardar como rechazado para no volver a ver
                    logger.info(f"   ❌ RECHAZADO (Score: {analysis['score']}) | {analysis.get('reason','')}")
                    continue
                
                logger.info(f"   ✅ ACEPTADO (Score: {analysis['score']})")
                
                ai_price = analysis.get('suggested_price')
                final_price = self.get_smart_price(p['url'], p['budget_text'], p['bids_count'], ai_price)
                
                success = self.fill_and_send_proposal(
                    p['url'], final_price, analysis['delivery_days'], analysis['proposal_text']
                )
                
                if success:
                    sent_count += 1
                    wait_time = random.randint(*Config.DELAY_BETWEEN_PROPOSALS)
                    logger.info(f"⏳ Esperando {wait_time//60} min para siguiente propuesta...")
                    time.sleep(wait_time)

        except Exception as e:
            logger.error(f"❌ Error fatal en ejecución: {e}")
            import traceback
            traceback.print_exc()
        finally:
            if hasattr(self, 'driver') and self.driver:
                logger.info("👋 Cerrando navegador.")
                self.driver.quit()
