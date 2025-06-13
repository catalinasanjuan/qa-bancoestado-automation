"""
Page Object Model para el Simulador de Crédito de BancoEstado
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import re


class SimuladorCreditoPage:
    """Page Object para el simulador de crédito de consumo"""
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)
    
    # LOCALIZADORES
    # Página principal
    BOTON_SIMULA_AQUI = (By.XPATH, "//a[contains(text(), 'Simula aquí') or contains(@class, 'simular')]")
    ENLACE_SIMULADOR = (By.XPATH, "//a[contains(@href, 'simulador') or contains(text(), 'Simulador')]")
    ENLACE_CREDITO_CONSUMO = (By.XPATH, "//a[contains(text(), 'Crédito de Consumo')]")
    
    # Formulario del simulador
    CAMPO_MONTO = (By.ID, "monto")
    CAMPO_MONTO_ALT = (By.XPATH, "//input[contains(@name, 'monto') or contains(@id, 'amount')]")
    
    CAMPO_CUOTAS = (By.ID, "cuotas")
    CAMPO_CUOTAS_ALT = (By.XPATH, "//select[contains(@name, 'cuota') or contains(@id, 'installment')]")
    
    BOTON_SIMULAR = (By.XPATH, "//button[contains(text(), 'Simular') or contains(@value, 'simular')]")
    BOTON_SIMULAR_ALT = (By.XPATH, "//input[@type='submit' and contains(@value, 'Simular')]")
    
    # Resultados
    CONTENEDOR_RESULTADOS = (By.CLASS_NAME, "resultados")
    CONTENEDOR_RESULTADOS_ALT = (By.XPATH, "//div[contains(@class, 'result') or contains(@class, 'simulacion')]")
    
    CUOTA_MENSUAL = (By.XPATH, "//span[contains(text(), 'Cuota') or contains(text(), 'cuota')]")
    TASA_CAE = (By.XPATH, "//span[contains(text(), 'CAE') or contains(text(), 'Tasa')]")
    COSTO_TOTAL = (By.XPATH, "//span[contains(text(), 'Total') or contains(text(), 'total')]")
    
    # Mensajes de error
    MENSAJE_ERROR = (By.XPATH, "//div[contains(@class, 'error') or contains(@class, 'alert')]")
    
    def abrir_pagina_principal(self, url):
        """Abre la página principal de BancoEstado"""
        print(f"Abriendo página: {url}")
        self.driver.get(url)
        self.driver.maximize_window()
        time.sleep(3)  # Esperar a que cargue completamente
        return self
    
    def ir_al_simulador(self):
        """Navega al simulador de crédito"""
        try:
            # Intentar encontrar el botón "Simula aquí"
            print("Buscando botón de simulador...")
            
            # Scroll hacia abajo para buscar el simulador
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
            time.sleep(2)
            
            # Intentar múltiples selectores
            selectores = [
                self.BOTON_SIMULA_AQUI,
                self.ENLACE_SIMULADOR,
                self.ENLACE_CREDITO_CONSUMO,
                (By.PARTIAL_LINK_TEXT, "Simula"),
                (By.PARTIAL_LINK_TEXT, "Crédito"),
                (By.XPATH, "//button[contains(text(), 'Simula')]"),
                (By.XPATH, "//a[contains(@href, 'credito')]")
            ]
            
            elemento_encontrado = None
            for selector in selectores:
                try:
                    elemento = self.wait.until(EC.element_to_be_clickable(selector))
                    elemento_encontrado = elemento
                    print(f"Elemento encontrado con selector: {selector}")
                    break
                except TimeoutException:
                    continue
            
            if elemento_encontrado:
                # Scroll al elemento y hacer clic
                self.driver.execute_script("arguments[0].scrollIntoView();", elemento_encontrado)
                time.sleep(1)
                
                try:
                    elemento_encontrado.click()
                except:
                    # Si el clic normal falla, usar JavaScript
                    self.driver.execute_script("arguments[0].click();", elemento_encontrado)
                
                print("Navegando al simulador...")
                time.sleep(3)
                return True
            else:
                print("No se pudo encontrar el botón del simulador")
                return False
                
        except Exception as e:
            print(f"Error al navegar al simulador: {str(e)}")
            return False
    
    def esta_en_simulador(self):
        """Verifica si estamos en la página del simulador"""
        try:
            # Buscar elementos característicos del simulador
            elementos_simulador = [
                self.CAMPO_MONTO,
                self.CAMPO_MONTO_ALT,
                (By.XPATH, "//input[contains(@placeholder, 'monto')]"),
                (By.XPATH, "//label[contains(text(), 'Monto')]")
            ]
            
            for elemento in elementos_simulador:
                try:
                    self.driver.find_element(*elemento)
                    return True
                except NoSuchElementException:
                    continue
            
            return False
        except Exception:
            return False
    
    def ingresar_monto(self, monto):
        """Ingresa el monto del crédito"""
        try:
            # Limpiar el monto y convertir a string sin formato
            monto_limpio = str(monto).replace('$', '').replace('.', '').replace(',', '')
            
            print(f"Ingresando monto: {monto_limpio}")
            
            # Intentar encontrar el campo de monto
            campo_monto = None
            selectores_monto = [
                self.CAMPO_MONTO,
                self.CAMPO_MONTO_ALT,
                (By.XPATH, "//input[contains(@placeholder, 'monto') or contains(@name, 'amount')]"),
                (By.XPATH, "//input[@type='text' or @type='number']")
            ]
            
            for selector in selectores_monto:
                try:
                    campo_monto = self.wait.until(EC.presence_of_element_located(selector))
                    break
                except TimeoutException:
                    continue
            
            if campo_monto:
                # Limpiar campo y ingresar monto
                campo_monto.clear()
                time.sleep(0.5)
                campo_monto.send_keys(monto_limpio)
                time.sleep(1)
                print(f"Monto {monto_limpio} ingresado correctamente")
                return True
            else:
                print("No se pudo encontrar el campo de monto")
                return False
                
        except Exception as e:
            print(f"Error al ingresar monto: {str(e)}")
            return False
    
    def seleccionar_cuotas(self, cuotas):
        """Selecciona el número de cuotas"""
        try:
            cuotas_str = str(cuotas)
            print(f"Seleccionando {cuotas_str} cuotas")
            
            # Intentar encontrar el campo de cuotas
            selectores_cuotas = [
                self.CAMPO_CUOTAS,
                self.CAMPO_CUOTAS_ALT,
                (By.XPATH, "//select[contains(@name, 'cuota')]"),
                (By.XPATH, "//select[contains(@id, 'plazo')]")
            ]
            
            campo_cuotas = None
            for selector in selectores_cuotas:
                try:
                    campo_cuotas = self.wait.until(EC.presence_of_element_located(selector))
                    break
                except TimeoutException:
                    continue
            
            if campo_cuotas:
                select = Select(campo_cuotas)
                
                # Intentar seleccionar por valor exacto
                try:
                    select.select_by_value(cuotas_str)
                except:
                    # Si falla, intentar por texto visible
                    try:
                        select.select_by_visible_text(cuotas_str)
                    except:
                        # Como último recurso, seleccionar por índice aproximado
                        opciones = select.options
                        for i, opcion in enumerate(opciones):
                            if cuotas_str in opcion.text:
                                select.select_by_index(i)
                                break
                
                time.sleep(1)
                print(f"Cuotas {cuotas_str} seleccionadas correctamente")
                return True
            else:
                print("No se pudo encontrar el campo de cuotas")
                return False
                
        except Exception as e:
            print(f"Error al seleccionar cuotas: {str(e)}")
            return False
    
    def hacer_clic_simular(self):
        """Hace clic en el botón simular"""
        try:
            print("Haciendo clic en botón Simular...")
            
            selectores_simular = [
                self.BOTON_SIMULAR,
                self.BOTON_SIMULAR_ALT,
                (By.XPATH, "//button[contains(text(), 'Calcular')]"),
                (By.XPATH, "//input[@type='submit']")
            ]
            
            boton_simular = None
            for selector in selectores_simular:
                try:
                    boton_simular = self.wait.until(EC.element_to_be_clickable(selector))
                    break
                except TimeoutException:
                    continue
            
            if boton_simular:
                # Scroll al botón
                self.driver.execute_script("arguments[0].scrollIntoView();", boton_simular)
                time.sleep(1)
                
                try:
                    boton_simular.click()
                except:
                    # Si falla, usar JavaScript
                    self.driver.execute_script("arguments[0].click();", boton_simular)
                
                print("Clic en Simular ejecutado")
                time.sleep(3)  # Esperar a que carguen los resultados
                return True
            else:
                print("No se pudo encontrar el botón Simular")
                return False
                
        except Exception as e:
            print(f"Error al hacer clic en Simular: {str(e)}")
            return False
    
    def obtener_resultados(self):
        """Obtiene los resultados de la simulación"""
        try:
            print("Obteniendo resultados de la simulación...")
            
            # Esperar a que aparezcan los resultados
            time.sleep(3)
            
            resultados = {}
            
            # Buscar elementos de resultados en toda la página
            texto_pagina = self.driver.page_source
            
            # Buscar cuota mensual
            patron_cuota = r'[\$]?([0-9]{1,3}(?:[.,][0-9]{3})*(?:[.,][0-9]{2})?)'
            patrones_cuota = [
                r'Cuota.*?[\$]?([0-9]{1,3}(?:[.,][0-9]{3})*)',
                r'cuota.*?[\$]?([0-9]{1,3}(?:[.,][0-9]{3})*)',
                r'Valor.*?[\$]?([0-9]{1,3}(?:[.,][0-9]{3})*)'
            ]
            
            # Buscar CAE
            patrones_cae = [
                r'CAE.*?([0-9]{1,2}[.,][0-9]{1,2})%?',
                r'Tasa.*?([0-9]{1,2}[.,][0-9]{1,2})%?'
            ]
            
            # Buscar costo total
            patrones_total = [
                r'Total.*?[\$]?([0-9]{1,3}(?:[.,][0-9]{3})*)',
                r'Costo.*?[\$]?([0-9]{1,3}(?:[.,][0-9]{3})*)'
            ]
            
            # Extraer información usando expresiones regulares
            for patron in patrones_cuota:
                match = re.search(patron, texto_pagina, re.IGNORECASE)
                if match:
                    resultados['cuota_mensual'] = match.group(1)
                    break
            
            for patron in patrones_cae:
                match = re.search(patron, texto_pagina, re.IGNORECASE)
                if match:
                    resultados['tasa_cae'] = match.group(1)
                    break
            
            for patron in patrones_total:
                match = re.search(patron, texto_pagina, re.IGNORECASE)
                if match:
                    resultados['costo_total'] = match.group(1)
                    break
            
            # Si no encontramos resultados con regex, buscar elementos visibles
            if not resultados:
                elementos_texto = self.driver.find_elements(By.XPATH, "//*[contains(text(), '$') or contains(text(), 'CAE')]")
                for elemento in elementos_texto:
                    texto = elemento.text
                    if '$' in texto and 'cuota' in texto.lower():
                        resultados['cuota_mensual'] = texto
                    elif 'CAE' in texto:
                        resultados['tasa_cae'] = texto
                    elif '$' in texto and 'total' in texto.lower():
                        resultados['costo_total'] = texto
            
            print(f"Resultados obtenidos: {resultados}")
            return resultados
            
        except Exception as e:
            print(f"Error al obtener resultados: {str(e)}")
            return {}
    
    def hay_resultados_visibles(self):
        """Verifica si hay resultados visibles en la página"""
        try:
            # Buscar indicadores de que hay resultados
            indicadores = [
                "cuota",
                "CAE",
                "total",
                "$",
                "peso",
                "resultado",
                "simulación"
            ]
            
            texto_pagina = self.driver.page_source.lower()
            
            # Si hay al menos 2 indicadores, probablemente hay resultados
            contador = 0
            for indicador in indicadores:
                if indicador in texto_pagina:
                    contador += 1
            
            return contador >= 2
            
        except Exception:
            return False
    
    def obtener_mensaje_error(self):
        """Obtiene el mensaje de error si existe"""
        try:
            selectores_error = [
                self.MENSAJE_ERROR,
                (By.XPATH, "//div[contains(@class, 'warning')]"),
                (By.XPATH, "//*[contains(text(), 'error') or contains(text(), 'Error')]")
            ]
            
            for selector in selectores_error:
                try:
                    elemento_error = self.driver.find_element(*selector)
                    return elemento_error.text
                except NoSuchElementException:
                    continue
            
            return None
            
        except Exception:
            return None