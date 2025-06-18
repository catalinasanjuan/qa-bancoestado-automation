"""
Configuracion del entorno para Behave
"""
import os
import sys
from datetime import datetime

# Agregar el directorio raiz al path de Python
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def before_all(context):
    """Configuracion que se ejecuta antes de todas las pruebas"""
    print("Iniciando suite de pruebas de BancoEstado...")
    print("=" * 60)

    # Configurar timestamp para reportes
    context.test_start_time = datetime.now()

    # Crear directorios necesarios
    directories = ['screenshots', 'allure_reports', 'reports']
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Directorio creado: {directory}")

def before_scenario(context, scenario):
    """Configuracion que se ejecuta antes de cada escenario"""
    print(f"\nEjecutando escenario: {scenario.name}")
    print("-" * 50)

    # Timestamp del escenario
    context.scenario_start_time = datetime.now()

    # Limpiar variables del contexto
    context.resultados = {}
    context.monto_ingresado = None
    context.cuotas_seleccionadas = None

def after_scenario(context, scenario):
    """Configuracion que se ejecuta despues de cada escenario"""
    scenario_duration = datetime.now() - context.scenario_start_time

    if scenario.status == "passed":
        print(f"Escenario EXITOSO: {scenario.name}")
        print(f"Duracion: {scenario_duration.total_seconds():.2f} segundos")
    else:
        print(f"Escenario FALLIDO: {scenario.name}")
        print(f"Duracion: {scenario_duration.total_seconds():.2f} segundos")

        # Tomar screenshot en caso de fallo
        if hasattr(context, 'driver_manager') and context.driver_manager:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_name = f"FAILED_{scenario.name.replace(' ', '_')}_{timestamp}.png"
            context.driver_manager.take_screenshot(screenshot_name)
            print(f"Screenshot guardado: {screenshot_name}")

    # Cerrar el driver despues de cada escenario
    if hasattr(context, 'driver_manager') and context.driver_manager:
        context.driver_manager.close_driver()
        print("Driver cerrado correctamente")

    print("-" * 50)

def after_all(context):
    """Configuracion que se ejecuta despues de todas las pruebas"""
    total_duration = datetime.now() - context.test_start_time

    print("\n" + "=" * 60)
    print("Suite de pruebas completada")
    print(f"Duracion total: {total_duration.total_seconds():.2f} segundos")
    print("=" * 60)

def before_feature(context, feature):
    """Configuracion que se ejecuta antes de cada feature"""
    print(f"\nFeature: {feature.name}")
    print(f"{feature.description}")

def after_step(context, step):
    """Configuracion que se ejecuta despues de cada step"""
    if step.status == "failed":
        print(f"Step fallido: {step.name}")

        # Informacion adicional para debug
        if hasattr(context, 'driver') and context.driver:
            print(f"URL actual: {context.driver.current_url}")
            print(f"Titulo de pagina: {context.driver.title}")
    elif step.status == "passed":
        print(f"Step exitoso: {step.name}")

    # Pausa entre steps
    import time
    time.sleep(0.5)
