"""
Configuración del entorno para Behave
"""
import os
import sys
from datetime import datetime

# Agregar el directorio raíz al path de Python
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def before_all(context):
    """Configuración que se ejecuta antes de todas las pruebas"""
    print("🚀 Iniciando suite de pruebas de BancoEstado...")
    print("=" * 60)
    
    # Configurar timestamp para reportes
    context.test_start_time = datetime.now()
    
    # Crear directorios necesarios
    directories = ['screenshots', 'allure_reports', 'reports']
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"📁 Directorio creado: {directory}")

def before_scenario(context, scenario):
    """Configuración que se ejecuta antes de cada escenario"""
    print(f"\n🧪 Ejecutando escenario: {scenario.name}")
    print("-" * 50)
    
    # Timestamp del escenario
    context.scenario_start_time = datetime.now()
    
    # Limpiar variables del contexto
    context.resultados = {}
    context.monto_ingresado = None
    context.cuotas_seleccionadas = None

def after_scenario(context, scenario):
    """Configuración que se ejecuta después de cada escenario"""
    scenario_duration = datetime.now() - context.scenario_start_time
    
    if scenario.status == "passed":
        print(f"✅ Escenario EXITOSO: {scenario.name}")
        print(f"⏱️  Duración: {scenario_duration.total_seconds():.2f} segundos")
    else:
        print(f"❌ Escenario FALLIDO: {scenario.name}")
        print(f"⏱️  Duración: {scenario_duration.total_seconds():.2f} segundos")
        
        # Tomar screenshot en caso de fallo
        if hasattr(context, 'driver_manager') and context.driver_manager:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_name = f"FAILED_{scenario.name.replace(' ', '_')}_{timestamp}.png"
            context.driver_manager.take_screenshot(screenshot_name)
            print(f"📸 Screenshot guardado: {screenshot_name}")
    
    # Cerrar el driver después de cada escenario
    if hasattr(context, 'driver_manager') and context.driver_manager:
        context.driver_manager.close_driver()
        print("🔒 Driver cerrado correctamente")
    
    print("-" * 50)

def after_all(context):
    """Configuración que se ejecuta después de todas las pruebas"""
    total_duration = datetime.now() - context.test_start_time
    
    print("\n" + "=" * 60)
    print("🏁 Suite de pruebas completada")
    print(f"⏱️  Duración total: {total_duration.total_seconds():.2f} segundos")
    print("=" * 60)

def before_feature(context, feature):
    """Configuración que se ejecuta antes de cada feature"""
    print(f"\n📋 Feature: {feature.name}")
    print(f"📄 {feature.description}")

def after_step(context, step):
    """Configuración que se ejecuta después de cada step"""
    if step.status == "failed":
        print(f"❌ Step fallido: {step.name}")
        
        # Información adicional para debug
        if hasattr(context, 'driver') and context.driver:
            print(f"🌐 URL actual: {context.driver.current_url}")
            print(f"📄 Título de página: {context.driver.title}")
    elif step.status == "passed":
        print(f"✅ Step exitoso: {step.name}")
    
    # Agregar pequeña pausa entre steps para estabilidad
    import time
    time.sleep(0.5)