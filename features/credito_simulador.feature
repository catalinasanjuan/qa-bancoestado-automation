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
    Y hago clic en el botón "Simular"
    Entonces debería ver los resultados de la simulación
    Y debería mostrar el valor de la cuota mensual
    Y debería mostrar la tasa CAE
    Y debería mostrar el costo total del crédito

  @regresion
  Escenario: Simulación con monto mínimo permitido
    Dado que estoy en el simulador de crédito
    Cuando ingreso un monto de "$620000"
    Y selecciono "12" cuotas
    Y hago clic en el botón "Simular"
    Entonces debería ver los resultados de la simulación
    Y debería mostrar el valor de la cuota mensual

  @regresion
  Escenario: Simulación con plazo máximo para cliente regular
    Dado que estoy en el simulador de crédito
    Cuando ingreso un monto de "$3000000"
    Y selecciono "60" cuotas
    Y hago clic en el botón "Simular"
    Entonces debería ver los resultados de la simulación
    Y debería mostrar el valor de la cuota mensual

  @validacion_calculos @critico
  Esquema del escenario: Validación de cálculos con diferentes montos y plazos
    Dado que estoy en el simulador de crédito
    Cuando ingreso un monto de "<monto>"
    Y selecciono "<cuotas>" cuotas
    Y hago clic en el botón "Simular"
    Entonces debería ver los resultados de la simulación
    Y el valor de la cuota mensual debería ser mayor a "0"
    Y la tasa CAE debería estar entre "0" y "100" por ciento
    Y el costo total debería ser mayor al monto solicitado

    Ejemplos:
      | monto    | cuotas |
      | $1000000 | 24     |
      | $2500000 | 36     |
      | $4000000 | 48     |
      | $6000000 | 60     |

  @error_handling
  Escenario: Validación de campos obligatorios
    Dado que estoy en el simulador de crédito
    Cuando dejo el campo de monto vacío
    Y hago clic en el botón "Simular"
    Entonces debería ver un mensaje de error indicando que el monto es obligatorio
    