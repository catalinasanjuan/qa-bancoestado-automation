"""
Page Object Model para el Simulador de Crédito de BancoEstado
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import ElementNotInteractableException, UnexpectedTagNameException

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
    
    # Modal de RUT
    CAMPO_RUT = (By.XPATH, "//input[@name='rut' or @placeholder='Ingresa tu RUT' or contains(@id, 'rut')]")
    BOTON_SIMULAR_RUT = (By.XPATH, "//button[contains(text(), 'Simular')]")
    
    # Formulario del simulador
    CAMPO_MONTO = (By.XPATH, "//input[@name='monto' or @id='ingresamonto' or contains(@placeholder, 'monto')]")
    CAMPO_CUOTAS = (By.XPATH, "//select[contains(@name, 'cuota') or contains(@id, 'cuota')]")
    
    # Fechas
    CAMPO_MES_PAGO = (By.XPATH, "//select[contains(@name, 'mes') or contains(text(), 'Septiembre')]")
    CAMPO_DIA_PAGO = (By.XPATH, "//select[contains(@name, 'dia') or contains(text(), '7')]")
    
    # Seguros
    RADIO_CON_SEGURO = (By.XPATH, "//input[@type='radio' and contains(@value, 'seguro')]")
    RADIO_SIN_SEGURO = (By.XPATH, "//input[@type='radio' and contains(@value, 'sin')]")
    
    # Botones
    BOTON_CONTINUAR = (By.XPATH, "//button[contains(text(), 'Continuar')]")
    
    # Resultados
    VALOR_CUOTA = (By.XPATH, "//*[contains(text(), 'Valor cuota')]/following-sibling::*")
    VALOR_CAE = (By.XPATH, "//*[contains(text(), 'CAE')]/following-sibling::*")
    COSTO_TOTAL = (By.XPATH, "//*[contains(text(), 'Costo Total del Crédito')]/following-sibling::*")

    def abrir_pagina_principal(self, url):
        """Abre la página principal de BancoEstado"""
        print(f"Abriendo página: {url}")
        self.driver.get(url)
        self.driver.maximize_window()
        time.sleep(3)  # Esperar a que cargue completamente
        return self
    
    def debug_buscar_elementos(self):
        """Función de debugging para explorar elementos en la página"""
        print("\n === INICIANDO DEBUGGING DE ELEMENTOS ===")
        
        try:
            # 1. Información básica de la página
            print(f"URL actual: {self.driver.current_url}")
            print(f"Título: {self.driver.title}")
            
            # 2. Buscar todos los elementos que contengan "simula"
            print("\n BUSCANDO ELEMENTOS CON 'SIMULA':")
            elementos_simula = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'simula') or contains(text(), 'Simula')]")
            
            for i, elemento in enumerate(elementos_simula):
                try:
                    if elemento.is_displayed():
                        print(f"  {i+1}. Tag: {elemento.tag_name}")
                        print(f"     Texto: '{elemento.text}'")
                        print(f"     ID: '{elemento.get_attribute('id')}'")
                        print(f"     Clase: '{elemento.get_attribute('class')}'")
                        print(f"     Href: '{elemento.get_attribute('href')}'")
                        print(f"     Clickeable: {elemento.tag_name in ['a', 'button'] or elemento.get_attribute('onclick')}")
                        print("     ---")
                except Exception as e:
                    print(f"     Error obteniendo info: {e}")
            
            # 3. Buscar todos los enlaces (a) y botones (button)
            print("\n BUSCANDO TODOS LOS ENLACES Y BOTONES:")
            enlaces_botones = self.driver.find_elements(By.XPATH, "//a | //button")
            
            elementos_relevantes = []
            for elemento in enlaces_botones:
                try:
                    if elemento.is_displayed():
                        texto = elemento.text.lower()
                        if 'simula' in texto or 'crédito' in texto or 'credito' in texto:
                            elementos_relevantes.append(elemento)
                except:
                    continue
            
            print(f"Encontrados {len(elementos_relevantes)} elementos relevantes:")
            for i, elemento in enumerate(elementos_relevantes):
                try:
                    print(f"  {i+1}. Tag: {elemento.tag_name}")
                    print(f"     Texto: '{elemento.text}'")
                    print(f"     ID: '{elemento.get_attribute('id')}'")
                    print(f"     Clase: '{elemento.get_attribute('class')}'")
                    print(f"     XPath sugerido: //{elemento.tag_name}[contains(text(), '{elemento.text[:20]}')]")
                    print("     ---")
                except Exception as e:
                    print(f"     Error: {e}")
            
            # 4. JavaScript para explorar elementos con estilos naranjas
            print("\n BUSCANDO ELEMENTOS NARANJAS CON JAVASCRIPT:")
            elementos_js = self.driver.execute_script("""
                var elementos = document.querySelectorAll('*');
                var resultados = [];
                
                for (var i = 0; i < elementos.length; i++) {
                    var elemento = elementos[i];
                    var texto = (elemento.textContent || elemento.innerText || '').toLowerCase();
                    var estilo = window.getComputedStyle(elemento);
                    
                    if (texto.includes('simula') || texto.includes('crédito') || texto.includes('credito')) {
                        resultados.push({
                            tagName: elemento.tagName,
                            texto: elemento.textContent || elemento.innerText || '',
                            id: elemento.id,
                            className: elemento.className,
                            backgroundColor: estilo.backgroundColor,
                            color: estilo.color,
                            display: estilo.display
                        });
                    }
                }
                
                return resultados.slice(0, 10); // Primeros 10 resultados
            """)
            
            for i, elemento in enumerate(elementos_js):
                print(f"  {i+1}. Tag: {elemento['tagName']}")
                print(f"     Texto: '{elemento['texto'][:50]}...'")
                print(f"     ID: '{elemento['id']}'")
                print(f"     Clase: '{elemento['className']}'")
                print(f"     Background: {elemento['backgroundColor']}")
                print(f"     Color: {elemento['color']}")
                print("     ---")
            
            # 5. Buscar elementos por secciones específicas
            print("\n BUSCANDO EN SECCIONES ESPECÍFICAS:")
            
            # Buscar sección de crédito de consumo
            try:
                seccion_credito = self.driver.find_element(By.XPATH, "//*[contains(text(), 'Crédito de Consumo')]")
                print(" Sección 'Crédito de Consumo' encontrada")
                
                # Buscar elementos clickeables cerca
                elementos_cercanos = self.driver.find_elements(By.XPATH, 
                    "//*[contains(text(), 'Crédito de Consumo')]/following::a[position()<=5] | " +
                    "//*[contains(text(), 'Crédito de Consumo')]/following::button[position()<=5]")
                
                print(f"Elementos clickeables cercanos: {len(elementos_cercanos)}")
                for i, elemento in enumerate(elementos_cercanos):
                    try:
                        if elemento.is_displayed():
                            print(f"  {i+1}. Texto: '{elemento.text}'")
                            print(f"     Tag: {elemento.tag_name}")
                            print(f"     Clase: '{elemento.get_attribute('class')}'")
                    except:
                        pass
                        
            except:
                print(" No se encontró sección 'Crédito de Consumo'")
            
            # 6. Capturar screenshot para análisis visual
            screenshot_path = "screenshots/debug_elementos_pagina.png"
            self.driver.save_screenshot(screenshot_path)
            print(f"\n📸 Screenshot guardado: {screenshot_path}")
            
            print("\n === FIN DEL DEBUGGING ===\n")
            
            return elementos_relevantes
            
        except Exception as e:
            print(f" Error durante debugging: {str(e)}")
            return []
    def ir_al_simulador(self):
        """Navega al simulador de crédito"""
        try:
            print("Buscando botón 'Simula tu Crédito'...")
            
            # Scroll hacia abajo para encontrar la sección del simulador
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
            time.sleep(3)
            
            boton_encontrado = None
            
            # Estrategia 1: Buscar el span "Simula aquí" y obtener su elemento padre clickeable
            try:
                span_simula = self.driver.find_element(By.XPATH, "//span[contains(text(), 'Simula aquí')]")
                if span_simula and span_simula.is_displayed():
                    print(" Encontrado span 'Simula aquí'")
                    
                    # Buscar el elemento padre clickeable (a o button)
                    try:
                        boton_padre = span_simula.find_element(By.XPATH, "./ancestor::a[1]")
                        if boton_padre:
                            boton_encontrado = boton_padre
                            print(f" Elemento padre clickeable encontrado: ID='{boton_padre.get_attribute('id')}', Clase='{boton_padre.get_attribute('class')}'")
                    except:
                        try:
                            boton_padre = span_simula.find_element(By.XPATH, "./ancestor::button[1]")
                            if boton_padre:
                                boton_encontrado = boton_padre
                                print(f" Botón padre encontrado: ID='{boton_padre.get_attribute('id')}'")
                        except:
                            # Si no encuentra padre clickeable, usar el span mismo
                            boton_encontrado = span_simula
                            print(" Usando el span directamente")
            except:
                print("No se encontró span 'Simula aquí'")
            
            # Estrategia 2: Buscar por ID específico encontrado en el debugging
            if not boton_encontrado:
                try:
                    boton_por_id = self.driver.find_element(By.ID, "button-5689690780")
                    if boton_por_id and boton_por_id.is_displayed():
                        boton_encontrado = boton_por_id
                        print(" Encontrado botón por ID específico")
                except:
                    print("No se encontró botón por ID")
            
            # Estrategia 3: Buscar por clase msd-button
            if not boton_encontrado:
                try:
                    botones_msd = self.driver.find_elements(By.XPATH, "//a[contains(@class, 'msd-button')]")
                    for boton in botones_msd:
                        if boton.is_displayed():
                            # Verificar si está cerca del texto "Simula"
                            try:
                                texto_cercano = boton.find_element(By.XPATH, ".//span[contains(text(), 'Simula')]")
                                if texto_cercano:
                                    boton_encontrado = boton
                                    print(f" Botón msd-button encontrado con texto 'Simula'")
                                    break
                            except:
                                continue
                except:
                    print("No se encontraron botones msd-button")
            
            # Estrategia 4: JavaScript para encontrar el botón que contiene "Simula aquí"
            if not boton_encontrado:
                try:
                    print("Buscando con JavaScript...")
                    resultado_js = self.driver.execute_script("""
                        // Buscar todos los elementos que contengan "Simula aquí"
                        var elementos = document.querySelectorAll('*');
                        for (var i = 0; i < elementos.length; i++) {
                            var elemento = elementos[i];
                            var texto = elemento.textContent || elemento.innerText || '';
                            
                            if (texto.includes('Simula aquí')) {
                                // Si es un span, buscar el elemento padre clickeable
                                if (elemento.tagName === 'SPAN') {
                                    var padre = elemento.closest('a, button');
                                    if (padre) {
                                        return padre;
                                    }
                                }
                                // Si ya es clickeable, devolverlo
                                if (elemento.tagName === 'A' || elemento.tagName === 'BUTTON') {
                                    return elemento;
                                }
                            }
                        }
                        
                        // Como alternativa, buscar por ID encontrado en debugging
                        var botonPorId = document.getElementById('button-5689690780');
                        if (botonPorId) {
                            return botonPorId;
                        }
                        
                        return null;
                    """)
                    
                    if resultado_js:
                        boton_encontrado = resultado_js
                        print(f" Botón encontrado por JavaScript")
                except Exception as e:
                    print(f"Error en JavaScript: {e}")
            
            if boton_encontrado:
                # Hacer clic en el botón encontrado
                self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", boton_encontrado)
                time.sleep(2)
                
                # Resaltar el elemento para debug
                self.driver.execute_script("arguments[0].style.border='3px solid red';", boton_encontrado)
                time.sleep(1)
                
                # Información del elemento antes de hacer clic
                print(f" Haciendo clic en elemento:")
                print(f"   Tag: {boton_encontrado.tag_name}")
                print(f"   ID: '{boton_encontrado.get_attribute('id')}'")
                print(f"   Clase: '{boton_encontrado.get_attribute('class')}'")
                print(f"   Texto: '{boton_encontrado.text}'")
                print(f"   Href: '{boton_encontrado.get_attribute('href')}'")
                
                try:
                    # Intentar clic normal primero
                    boton_encontrado.click()
                    print(" Clic normal exitoso")
                except:
                    try:
                        # Si falla, usar JavaScript
                        self.driver.execute_script("arguments[0].click();", boton_encontrado)
                        print(" Clic JavaScript exitoso")
                    except:
                        print(" No se pudo hacer clic en el elemento")
                        return False
                
                time.sleep(5)  # Esperar a que cargue
                
                # Verificar si cambió la URL o apareció un modal
                nueva_url = self.driver.current_url
                print(f" URL después del clic: {nueva_url}")
                
                return True
            else:
                print(" No se encontró ningún elemento clickeable")
                return False
                
        except Exception as e:
            print(f"Error al buscar simulador: {str(e)}")
            return False
    
    def ingresar_rut(self, rut="21123191-2"):
        """Ingresa el RUT en el modal inicial"""
        try:
            print(f"Ingresando RUT: {rut}")
            
            # Esperar a que aparezca el modal de RUT
            time.sleep(2)
            
            # Buscar el campo de RUT
            campo_rut = None
            selectores_rut = [
                (By.XPATH, "//input[@name='rut']"),
                (By.XPATH, "//input[contains(@placeholder, 'RUT')]"),
                (By.XPATH, "//input[contains(@placeholder, 'rut')]"),
                (By.XPATH, "//input[@type='text']")
            ]
            
            for selector in selectores_rut:
                try:
                    campo_rut = self.driver.find_element(*selector)
                    if campo_rut.is_displayed():
                        break
                except:
                    continue
            
            if campo_rut:
                campo_rut.clear()
                campo_rut.send_keys(rut)
                print(f" RUT {rut} ingresado correctamente")
                time.sleep(1)
                return True
            else:
                print(" No se encontró el campo de RUT")
                return False
                
        except Exception as e:
            print(f"Error al ingresar RUT: {str(e)}")
            return False
    
    def hacer_clic_simular_rut(self):
        """Hace clic en el botón Simular del modal de RUT"""
        try:
            print("Haciendo clic en botón Simular (modal RUT)...")
            
            # Buscar el botón Simular en el modal
            boton_simular = None
            selectores = [
                (By.XPATH, "//button[contains(text(), 'Simular')]"),
                (By.XPATH, "//input[@type='submit']"),
                (By.XPATH, "//button[@type='submit']")
            ]
            
            for selector in selectores:
                try:
                    boton_simular = self.driver.find_element(*selector)
                    if boton_simular.is_displayed():
                        break
                except:
                    continue
            
            if boton_simular:
                try:
                    boton_simular.click()
                except:
                    self.driver.execute_script("arguments[0].click();", boton_simular)
                
                print(" Clic en Simular (RUT) exitoso")
                time.sleep(3)
                return True
            else:
                print(" No se encontró el botón Simular")
                return False
                
        except Exception as e:
            print(f"Error al hacer clic en Simular: {str(e)}")
            return False
    
    def esta_en_simulador(self):
        """Verifica si estamos en la página del simulador"""
        try:
            # Buscar elementos característicos del simulador
            elementos_simulador = [
                (By.XPATH, "//input[contains(@name, 'monto')]"),
                (By.XPATH, "//select[contains(@name, 'cuota')]"),
                (By.XPATH, "//h1[contains(text(), 'Simulación')]"),
                (By.XPATH, "//*[contains(text(), 'Ingresa el monto')]")
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
        """Ingresa el monto del crédito en el formulario principal"""
        try:
            monto_limpio = str(monto).replace('$', '').replace('.', '').replace(',', '')
            print(f"Ingresando monto: ${monto_limpio}")
            
            # Buscar el campo de monto en el formulario principal
            campo_monto = None
            selectores_monto = [
                (By.XPATH, "//input[@name='monto']"),
                (By.XPATH, "//input[@id='ingresamonto']"),
                (By.XPATH, "//input[contains(@placeholder, 'monto')]"),
                (By.XPATH, "//input[@type='text' and contains(@class, 'input')]")
            ]
            
            for selector in selectores_monto:
                try:
                    campo_monto = self.driver.find_element(*selector)
                    if campo_monto.is_displayed():
                        break
                except:
                    continue
            
            if campo_monto:
                # Limpiar y llenar el campo
                campo_monto.clear()
                time.sleep(0.5)
                campo_monto.send_keys(monto_limpio)
                time.sleep(1)
                print(f" Monto ${monto_limpio} ingresado correctamente")
                return True
            else:
                print(" No se encontró el campo de monto")
                return False
                
        except Exception as e:
            print(f"Error al ingresar monto: {str(e)}")
            return False
    

    
    def seleccionar_cuotas(self, cuotas):
        """Selecciona el número de cuotas desde un <select> nativo con espera robusta"""
        try:
            cuotas_str = str(cuotas)
            print(f" Seleccionando {cuotas_str} cuotas")

            # Esperar a que el <select> esté presente y visible
            select_elem = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, "//select[contains(@formcontrolname, 'numeroCuotas')]")
            ))

            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//select[contains(@formcontrolname, 'numeroCuotas')]")))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", select_elem)
            time.sleep(1)

            # Seleccionar usando Select de Selenium
            try:
                select = Select(select_elem)
                select.select_by_value(cuotas_str)
            except UnexpectedTagNameException:
                print(" Elemento no es un <select>. ¿Framework JS lo cambió?")
                return False
            except ElementNotInteractableException as e:
                print(f" Elemento no interactuable: {e}")
                return False

            print(f" Cuotas {cuotas_str} seleccionadas correctamente")
            return True

        except Exception as e:
            print(f" Error inesperado al seleccionar cuotas: {e}")
            self.driver.save_screenshot("screenshots/error_cuotas_dropdown.png")
            return False
   
   
    def completar_campos_obligatorios(self):
        """Completa los campos requeridos para habilitar el botón Continuar"""
        try:
            print(" Seleccionando mes: Agosto")
            select_mes = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, "//select[@formcontrolname='mesPago']")
            ))
            Select(select_mes).select_by_visible_text("Agosto")

            print(" Seleccionando día: 7")
            select_dia = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, "//select[@formcontrolname='diaPago']")
            ))
            Select(select_dia).select_by_visible_text("7")

            print(" Seleccionando seguro: Desgravamen")
            radio_seguro = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//input[@type='radio' and @value='14IV']")
            ))
            self.driver.execute_script("arguments[0].click();", radio_seguro)  # JS click por robustez

            time.sleep(1)
            print(" Campos obligatorios completados")
            return True

        except Exception as e:
            print(f" Error al completar campos obligatorios: {e}")
            self.driver.save_screenshot("screenshots/error_campos_obligatorios.png")
            raise AssertionError("Error al seleccionar mes")  # para Behave



    
    def hacer_clic_continuar(self):
        """Hace clic en el botón Continuar del formulario"""
        try:
            print("Haciendo clic en botón Continuar...")
            
            # Buscar el botón Continuar
            boton_continuar = None
            selectores = [
                (By.XPATH, "//button[contains(text(), 'Continuar')]"),
                (By.XPATH, "//input[@value='Continuar']"),
                (By.XPATH, "//button[@type='submit']")
            ]
            
            for selector in selectores:
                try:
                    boton_continuar = self.driver.find_element(*selector)
                    if boton_continuar.is_displayed():
                        break
                except:
                    continue
            
            if boton_continuar:
                # Scroll al botón y hacer clic
                self.driver.execute_script("arguments[0].scrollIntoView(true);", boton_continuar)
                time.sleep(1)
                
                try:
                    boton_continuar.click()
                except:
                    self.driver.execute_script("arguments[0].click();", boton_continuar)
                
                print(" Clic en Continuar exitoso")
                time.sleep(3)
                return True
            else:
                print(" No se encontró el botón Continuar")
                return False
                
        except Exception as e:
            print(f"Error al hacer clic en Continuar: {str(e)}")
            return False
    
    def obtener_resultados(self):
        """Obtiene los resultados de la simulación"""
        try:
            print("📊¿ Obteniendo resultados de la simulación...")
            time.sleep(3)
            
            resultados = {}
            
            # Buscar información específica de los resultados
            try:
                # Valor de la cuota
                cuota_element = self.driver.find_element(By.XPATH, "//*[contains(text(), '$93.525') or contains(text(), 'Valor cuota')]")
                if cuota_element:
                    resultados['cuota_mensual'] = cuota_element.text
                    print(f" Cuota encontrada: {cuota_element.text}")
            except:
                pass
            
            try:
                # CAE
                cae_element = self.driver.find_element(By.XPATH, "//*[contains(text(), '32.88%') or contains(text(), 'CAE')]")
                if cae_element:
                    resultados['tasa_cae'] = cae_element.text
                    print(f" CAE encontrada: {cae_element.text}")
            except:
                pass
            
            try:
                # Costo total
                total_element = self.driver.find_element(By.XPATH, "//*[contains(text(), '$935.249') or contains(text(), 'Costo Total')]")
                if total_element:
                    resultados['costo_total'] = total_element.text
                    print(f" Costo total encontrado: {total_element.text}")
            except:
                pass
            
            # Si no encuentra elementos específicos, buscar en todo el texto
            if not resultados:
                texto_pagina = self.driver.page_source
                if any(indicador in texto_pagina for indicador in ['$93.525', '32.88%', '$935.249', 'Valor cuota', 'CAE']):
                    resultados['simulacion_exitosa'] = True
                    print(" Resultados detectados en la página")
            
            return resultados
            
        except Exception as e:
            print(f"Error al obtener resultados: {str(e)}")
            return {}
    
    def hay_resultados_visibles(self):
        """Verifica si hay resultados visibles en la página"""
        try:
            # Verificar si estamos en la página de resultados
            url_actual = self.driver.current_url
            if 'simulador' in url_actual:
                # Buscar elementos característicos de resultados
                elementos_resultado = [
                    "Valor cuota", "CAE", "Costo Total", "$93.525", "32.88%", "$935.249",
                    "Este es el detalle del crédito", "Primer pago", "Número de cuotas"
                ]
                
                texto_pagina = self.driver.page_source
                resultados_encontrados = 0
                
                for elemento in elementos_resultado:
                    if elemento in texto_pagina:
                        resultados_encontrados += 1
                
                return resultados_encontrados >= 3  # Al menos 3 indicadores de resultados
            
            return False
            
        except Exception:
            return False
    
    def obtener_mensaje_error(self):
        """Obtiene el mensaje de error si existe"""
        try:
            selectores_error = [
                (By.XPATH, "//div[contains(@class, 'error') or contains(@class, 'alert')]"),
                (By.XPATH, "//div[contains(@class, 'warning')]"),
                (By.XPATH, "//*[contains(text(), 'error') or contains(text(), 'Error')]")
            ]
            
            for selector in selectores_error:
                try:
                    elemento_error = self.driver.find_element(*selector)
                    return elemento_error.text
                except:
                    continue
            
            return None
            
        except Exception:
            return None