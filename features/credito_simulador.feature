# language: es
@simulador_credito
Característica: Simulador de Crédito de Consumo BancoEstado
  Como cliente potencial de BancoEstado
  Quiero simular un crédito de consumo
  Para conocer las condiciones de financiamiento antes de solicitarlo

  Antecedentes:
    Dado que estoy en la página principal de BancoEstado
    Cuando accedo al simulador de crédito de consumo

  @smoke @critico
  Escenario: Simulación exitosa de crédito de consumo con valores válidos
    Dado que estoy en el simulador de crédito
    Cuando ingreso un monto de "$5000000"
    Y selecciono "48" cuotas
    Y completo los campos obligatorios del simulador
    Y hago clic en el botón "Continuar"
    Entonces debería ver los resultados de la simulación
    Y debería mostrar el valor de la cuota mensual
    Y debería mostrar la tasa CAE
    Y debería mostrar el costo total del crédito

  @regresion
  Escenario: Simulación con monto mínimo permitido
    Dado que estoy en el simulador de crédito
    Cuando ingreso un monto de "$620000"
    Y selecciono "12" cuotas
    Y completo los campos obligatorios del simulador
    Y hago clic en el botón "Continuar"
    Entonces debería ver los resultados de la simulación
    Y debería mostrar el valor de la cuota mensual

  @error_handling
  Escenario: Validación de campos obligatorios
    Dado que estoy en el simulador de crédito
    Cuando dejo el campo de monto vacío
    Y hago clic en el botón "Continuar"
    Entonces debería ver un mensaje de error indicando que el monto es obligatorio
