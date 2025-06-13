"""
Administrador de WebDriver para las pruebas de automatización
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import os

class DriverManager:
    """Clase para manejar la configuración y ciclo de vida del WebDriver"""
    
    def __init__(self, headless=False, window_size="1920,1080"):
        self.driver = None
        self.headless = headless
        self.window_size = window_size
        self.wait_timeout = 10
        
    def get_driver(self):
        """Inicializa y retorna una instancia de WebDriver configurada"""
        if self.driver is None:
            self.driver = self._create_chrome_driver()
        return self.driver
    
    def _create_chrome_driver(self):
        """Crea y configura el driver de Chrome"""
        chrome_options = Options()
        
        # Configuraciones básicas
        chrome_options.add_argument(f"--window-size={self.window_size}")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--allow-running-insecure-content")
        
        # Configurar idioma en español
        chrome_options.add_argument("--lang=es-CL")
        chrome_options.add_experimental_option('prefs', {
            'intl.accept_languages': 'es-CL,es,en'
        })
        
        # Modo headless si se especifica
        if self.headless:
            chrome_options.add_argument("--headless")
            
        # Configuraciones adicionales para estabilidad
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        try:
            # Intentar con WebDriver Manager
            print("🔄 Descargando ChromeDriver...")
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
        except Exception as e:
            print(f"❌ Error con WebDriver Manager: {e}")
            try:
                # Intentar con driver local si existe
                local_driver_path = os.path.join("drivers", "chromedriver.exe")
                if os.path.exists(local_driver_path):
                    print("🔄 Usando ChromeDriver local...")
                    service = Service(local_driver_path)
                    driver = webdriver.Chrome(service=service, options=chrome_options)
                else:
                    # Como último recurso, intentar sin especificar path
                    print("🔄 Intentando con ChromeDriver del sistema...")
                    driver = webdriver.Chrome(options=chrome_options)
            except Exception as e2:
                raise Exception(f"No se pudo inicializar ChromeDriver. Error: {e2}")
        
        # Configuraciones del driver
        driver.implicitly_wait(self.wait_timeout)
        driver.set_page_load_timeout(30)
        driver.maximize_window()
        
        # Ejecutar script para evitar detección de automatización
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        print("✅ ChromeDriver iniciado correctamente")
        return driver
    
    def get_wait(self, timeout=None):
        """Retorna una instancia de WebDriverWait"""
        timeout = timeout or self.wait_timeout
        return WebDriverWait(self.get_driver(), timeout)
    
    def wait_for_element(self, locator, timeout=None):
        """Espera a que un elemento sea visible"""
        return self.get_wait(timeout).until(
            EC.visibility_of_element_located(locator)
        )
    
    def wait_for_element_clickable(self, locator, timeout=None):
        """Espera a que un elemento sea clickeable"""
        return self.get_wait(timeout).until(
            EC.element_to_be_clickable(locator)
        )
    
    def close_driver(self):
        """Cierra el driver y limpia los recursos"""
        if self.driver:
            try:
                self.driver.quit()
            except Exception as e:
                print(f"Error al cerrar el driver: {e}")
            finally:
                self.driver = None
    
    def take_screenshot(self, filename):
        """Toma una captura de pantalla"""
        if self.driver:
            screenshots_dir = "screenshots"
            if not os.path.exists(screenshots_dir):
                os.makedirs(screenshots_dir)
            
            filepath = os.path.join(screenshots_dir, filename)
            self.driver.save_screenshot(filepath)
            return filepath
        return None