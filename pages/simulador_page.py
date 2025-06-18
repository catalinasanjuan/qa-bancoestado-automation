from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException, NoSuchElementException,
    ElementNotInteractableException, UnexpectedTagNameException
)
import time


class SimuladorCreditoPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    def abrir_pagina_principal(self, url):
        self.driver.get(url)
        self.driver.maximize_window()
        time.sleep(3)

    def ir_al_simulador(self):
        try:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
            time.sleep(3)

            boton = None

            try:
                span_simula = self.driver.find_element(By.XPATH, "//span[contains(text(), 'Simula aqui')]")
                boton = span_simula.find_element(By.XPATH, "./ancestor::a[1]")
            except:
                try:
                    boton = self.driver.find_element(By.ID, "button-5689690780")
                except:
                    pass

            if boton:
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", boton)
                time.sleep(2)
                try:
                    boton.click()
                except:
                    self.driver.execute_script("arguments[0].click();", boton)
                time.sleep(5)
                return True
            return False
        except Exception:
            return False

    def ingresar_rut(self, rut="21123191-2"):
        try:
            time.sleep(2)
            campo = None
            opciones = [
                (By.XPATH, "//input[@name='rut']"),
                (By.XPATH, "//input[contains(@placeholder, 'RUT')]"),
                (By.XPATH, "//input[@type='text']")
            ]
            for sel in opciones:
                try:
                    campo = self.driver.find_element(*sel)
                    if campo.is_displayed():
                        break
                except:
                    continue
            if campo:
                campo.clear()
                campo.send_keys(rut)
                time.sleep(1)
                return True
            return False
        except Exception:
            return False

    def hacer_clic_simular_rut(self):
        try:
            boton = None
            opciones = [
                (By.XPATH, "//button[contains(text(), 'Simular')]"),
                (By.XPATH, "//input[@type='submit']"),
                (By.XPATH, "//button[@type='submit']")
            ]
            for sel in opciones:
                try:
                    boton = self.driver.find_element(*sel)
                    if boton.is_displayed():
                        break
                except:
                    continue
            if boton:
                try:
                    boton.click()
                except:
                    self.driver.execute_script("arguments[0].click();", boton)
                time.sleep(3)
                return True
            return False
        except Exception:
            return False

    def esta_en_simulador(self):
        try:
            elementos = [
                (By.XPATH, "//input[contains(@name, 'monto')]"),
                (By.XPATH, "//select[contains(@name, 'cuota')]"),
                (By.XPATH, "//h1[contains(text(), 'Simulacion')]"),
                (By.XPATH, "//*[contains(text(), 'Ingresa el monto')]")
            ]
            for sel in elementos:
                try:
                    self.driver.find_element(*sel)
                    return True
                except NoSuchElementException:
                    continue
            return False
        except:
            return False

    def ingresar_monto(self, monto):
        try:
            monto = str(monto).replace('$', '').replace('.', '').replace(',', '')
            campo = None
            opciones = [
                (By.XPATH, "//input[@name='monto']"),
                (By.XPATH, "//input[@id='ingresamonto']"),
                (By.XPATH, "//input[contains(@placeholder, 'monto')]")
            ]
            for sel in opciones:
                try:
                    campo = self.driver.find_element(*sel)
                    if campo.is_displayed():
                        break
                except:
                    continue
            if campo:
                campo.clear()
                time.sleep(0.5)
                campo.send_keys(monto)
                time.sleep(1)
                return True
            return False
        except:
            return False

    def seleccionar_cuotas(self, cuotas):
        try:
            cuotas = str(cuotas)
            select_elem = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, "//select[contains(@formcontrolname, 'numeroCuotas')]")
            ))
            self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//select[contains(@formcontrolname, 'numeroCuotas')]")
            ))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", select_elem)
            time.sleep(1)
            Select(select_elem).select_by_value(cuotas)
            return True
        except:
            return False

    def completar_campos_obligatorios(self):
        try:
            select_mes = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, "//select[@formcontrolname='mesPago']")
            ))
            Select(select_mes).select_by_visible_text("Agosto")

            select_dia = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, "//select[@formcontrolname='diaPago']")
            ))
            Select(select_dia).select_by_visible_text("7")

            radio_seguro = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//input[@type='radio' and @value='14IV']")
            ))
            self.driver.execute_script("arguments[0].click();", radio_seguro)
            time.sleep(1)
            return True
        except:
            return False

    def hacer_clic_continuar(self):
        try:
            boton = None
            opciones = [
                (By.XPATH, "//button[contains(text(), 'Continuar')]"),
                (By.XPATH, "//input[@value='Continuar']"),
                (By.XPATH, "//button[@type='submit']")
            ]
            for sel in opciones:
                try:
                    boton = self.driver.find_element(*sel)
                    if boton.is_displayed():
                        break
                except:
                    continue
            if boton:
                self.driver.execute_script("arguments[0].scrollIntoView(true);", boton)
                time.sleep(1)
                try:
                    boton.click()
                except:
                    self.driver.execute_script("arguments[0].click();", boton)
                time.sleep(3)
                return True
            return False
        except:
            return False

    def obtener_resultados(self):
        try:
            time.sleep(3)
            resultados = {}
            texto = self.driver.page_source
            if any(x in texto for x in ['Valor cuota', 'CAE', 'Costo Total']):
                resultados['simulacion_exitosa'] = True
            return resultados
        except:
            return {}

    def hay_resultados_visibles(self):
        try:
            texto = self.driver.page_source
            indicadores = ["Valor cuota", "CAE", "Costo Total", "detalle del credito", "Primer pago"]
            return sum([1 for i in indicadores if i in texto]) >= 3
        except:
            return False

    def obtener_mensaje_error(self):
        try:
            selectores = [
                (By.XPATH, "//div[contains(@class, 'error') or contains(@class, 'alert')]"),
                (By.XPATH, "//div[contains(@class, 'warning')]"),
                (By.XPATH, "//*[contains(text(), 'error') or contains(text(), 'Error')]")
            ]
            for sel in selectores:
                try:
                    el = self.driver.find_element(*sel)
                    return el.text
                except:
                    continue
            return None
        except:
            return None
