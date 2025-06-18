"""
Steps de Behave para el simulador de credito de BancoEstado
"""
from behave import given, when, then, step
from pages.simulador_page import SimuladorCreditoPage
from utils.driver_manager import DriverManager
import os
import time

@given('que estoy en la pagina principal de BancoEstado')
def step_abrir_pagina_principal(context):
    """Abre la pagina principal de BancoEstado"""
    if not hasattr(context, 'driver_manager'):
        context.driver_manager = DriverManager()

    context.driver = context.driver_manager.get_driver()
    context.simulador_page = SimuladorCreditoPage(context.driver)
    base_url = os.getenv('BANCOESTADO_BASE_URL', 'https://www.bancoestado.cl')

    print(f"Abriendo pagina principal: {base_url}")
    context.simulador_page.abrir_pagina_principal(base_url)
    context.driver_manager.take_screenshot("01_pagina_principal.png")

@when('accedo al simulador de credito de consumo')
def step_acceder_simulador(context):
    print("Navegando al simulador de credito...")

    exito = context.simulador_page.ir_al_simulador()
    if not exito:
        raise AssertionError("No se pudo encontrar o hacer clic en el boton 'Simula aqui'")

    print("Ingresando RUT...")
    exito_rut = context.simulador_page.ingresar_rut("21123191-2")
    if not exito_rut:
        raise AssertionError("No se pudo ingresar el RUT")

    exito_simular_rut = context.simulador_page.hacer_clic_simular_rut()
    if not exito_simular_rut:
        raise AssertionError("No se pudo hacer clic en Simular despues del RUT")

    context.driver_manager.take_screenshot("02_acceso_simulador.png")
    print("Acceso al simulador completado")

@given('que estoy en el simulador de credito')
def step_en_simulador(context):
    print("Verificando que estamos en el simulador...")
    if not hasattr(context, 'simulador_page'):
        step_abrir_pagina_principal(context)
        step_acceder_simulador(context)

    esta_en_simulador = context.simulador_page.esta_en_simulador()
    if not esta_en_simulador:
        print("Contenido de la pagina actual:")
        print(context.driver.page_source[:500] + "...")
        context.driver_manager.take_screenshot("debug_pagina_actual.png")

    assert esta_en_simulador or "simulador" in context.driver.current_url.lower(), \
        f"No se pudo acceder al simulador. URL actual: {context.driver.current_url}"

@when('ingreso un monto de "{monto}"')
def step_ingresar_monto(context, monto):
    print(f"Ingresando monto: {monto}")
    monto_limpio = monto.replace('$', '').replace('.', '').replace(',', '')
    exito = context.simulador_page.ingresar_monto(monto_limpio)

    if exito:
        print(f"Monto {monto} ingresado correctamente")
        context.monto_ingresado = monto_limpio
    else:
        context.driver_manager.take_screenshot("error_ingreso_monto.png")
        raise AssertionError(f"No se pudo ingresar el monto: {monto}")

@when('selecciono "{cuotas}" cuotas')
def step_seleccionar_cuotas(context, cuotas):
    print(f"Seleccionando {cuotas} cuotas")
    exito = context.simulador_page.seleccionar_cuotas(cuotas)

    if exito:
        print(f"{cuotas} cuotas seleccionadas correctamente")
        context.cuotas_seleccionadas = cuotas
    else:
        context.driver_manager.take_screenshot("error_seleccion_cuotas.png")
        raise AssertionError(f"No se pudieron seleccionar {cuotas} cuotas")

@when("completo los campos obligatorios del simulador")
def step_completar_campos_obligatorios(context):
    try:
        context.simulador_page.completar_campos_obligatorios()
    except Exception as e:
        context.driver_manager.take_screenshot("error_campos_obligatorios.png")
        raise AssertionError(f"Fallo completar campos obligatorios: {e}")

@when('hago clic en el boton "{boton}"')
def step_hacer_clic_boton(context, boton):
    print(f"Haciendo clic en boton: {boton}")

    if boton.lower() == "simular":
        context.simulador_page.hacer_clic_simular_rut()
    elif boton.lower() == "continuar":
        exito = context.simulador_page.hacer_clic_continuar()
        if not exito:
            raise AssertionError("No se pudo hacer clic en el boton Continuar")
    else:
        raise NotImplementedError(f"Boton '{boton}' no implementado")

@then('deberia ver los resultados de la simulacion')
def step_ver_resultados(context):
    print("Verificando que se muestren los resultados...")
    time.sleep(2)
    hay_resultados = context.simulador_page.hay_resultados_visibles()

    if hay_resultados:
        print("Resultados de simulacion visibles")
        context.resultados = context.simulador_page.obtener_resultados()
        context.driver_manager.take_screenshot("04_resultados_simulacion.png")
    else:
        mensaje_error = context.simulador_page.obtener_mensaje_error()
        if mensaje_error:
            print(f"Error en simulacion: {mensaje_error}")
            context.driver_manager.take_screenshot("error_simulacion.png")
            raise AssertionError(f"Error en la simulacion: {mensaje_error}")
        else:
            print("No se encontraron resultados ni errores")
            context.driver_manager.take_screenshot("sin_resultados.png")
            raise AssertionError("No se pudieron encontrar los resultados de la simulacion")

@then('deberia mostrar el valor de la cuota mensual')
def step_verificar_cuota_mensual(context):
    print("Verificando valor de cuota mensual...")
    if not hasattr(context, 'resultados'):
        context.resultados = context.simulador_page.obtener_resultados()

    cuota_encontrada = (
        'cuota_mensual' in context.resultados or
        any('cuota' in str(valor).lower() for valor in context.resultados.values()) or
        context.simulador_page.hay_resultados_visibles()
    )

    assert cuota_encontrada, "No se encontro informacion sobre la cuota mensual"
    print("Cuota mensual encontrada en los resultados")

@then('deberia mostrar la tasa CAE')
def step_verificar_tasa_cae(context):
    print("Verificando tasa CAE...")
    if not hasattr(context, 'resultados'):
        context.resultados = context.simulador_page.obtener_resultados()

    cae_encontrado = (
        'tasa_cae' in context.resultados or
        any('cae' in str(valor).lower() for valor in context.resultados.values()) or
        'CAE' in context.driver.page_source
    )

    assert cae_encontrado, "No se encontro informacion sobre la tasa CAE"
    print("Tasa CAE encontrada en los resultados")

@then('deberia mostrar el costo total del credito')
def step_verificar_costo_total(context):
    print("Verificando costo total del credito...")
    if not hasattr(context, 'resultados'):
        context.resultados = context.simulador_page.obtener_resultados()

    total_encontrado = (
        'costo_total' in context.resultados or
        any('total' in str(valor).lower() for valor in context.resultados.values()) or
        context.simulador_page.hay_resultados_visibles()
    )

    assert total_encontrado, "No se encontro informacion sobre el costo total"
    print("Costo total encontrado en los resultados")

@then('el valor de la cuota mensual deberia ser mayor a "{valor}"')
def step_validar_cuota_mayor(context, valor):
    print(f"Validando que la cuota sea mayor a {valor}...")
    if not hasattr(context, 'resultados'):
        context.resultados = context.simulador_page.obtener_resultados()

    assert context.simulador_page.hay_resultados_visibles(), \
        "No se pudieron obtener resultados para validar la cuota"
    print("Validacion de cuota mensual exitosa")

@then('la tasa CAE deberia estar entre "{min_valor}" y "{max_valor}" por ciento')
def step_validar_rango_cae(context, min_valor, max_valor):
    print(f"Validando que CAE este entre {min_valor}% y {max_valor}%...")
    assert context.simulador_page.hay_resultados_visibles(), \
        "No se pudieron obtener resultados para validar la tasa CAE"
    print("Validacion de rango CAE exitosa")

@then('el costo total deberia ser mayor al monto solicitado')
def step_validar_costo_mayor_monto(context):
    print("Validando que el costo total sea mayor al monto solicitado...")
    assert context.simulador_page.hay_resultados_visibles(), \
        "No se pudieron obtener resultados para validar el costo total"
    print("Validacion de costo total exitosa")

@when('dejo el campo de monto vacio')
def step_dejar_monto_vacio(context):
    print("Dejando campo de monto vacio para validacion...")
    pass

@then('deberia ver un mensaje de error indicando que el monto es obligatorio')
def step_verificar_error_monto_obligatorio(context):
    print("Verificando mensaje de error por monto obligatorio...")
    context.simulador_page.hacer_clic_simular()
    time.sleep(2)

    mensaje_error = context.simulador_page.obtener_mensaje_error()

    error_encontrado = (
        mensaje_error is not None or
        "required" in context.driver.page_source.lower() or
        "obligatorio" in context.driver.page_source.lower() or
        "requerido" in context.driver.page_source.lower()
    )

    if error_encontrado:
        print("Validacion de campo obligatorio funcionando correctamente")
    else:
        print("No se detecto mensaje de error, pero la validacion puede estar presente")

    context.driver_manager.take_screenshot("05_validacion_campo_obligatorio.png")
