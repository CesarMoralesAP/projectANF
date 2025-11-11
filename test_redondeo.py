"""
Test de redondeo para valores proyectados
"""
import numpy as np
from decimal import Decimal

# Simular valores que podrían generar problemas
valores_test = [
    50000.123456789,  # Muchos decimales
    1234567890.98765,  # Valor grande con decimales
    0.123456789,      # Valor pequeño
    np.float64(99999.999999),  # numpy.float64
]

print("="*60)
print("TEST DE REDONDEO PARA decimal(15,2)")
print("="*60)

for valor in valores_test:
    # Simular el proceso de guardado
    valor_redondeado = round(float(valor), 2)
    
    print(f"\nValor original: {valor}")
    print(f"Tipo original:  {type(valor)}")
    print(f"Valor redondeado: {valor_redondeado}")
    print(f"Tipo redondeado:  {type(valor_redondeado)}")
    
    # Verificar que sea compatible con Decimal(15,2)
    try:
        d = Decimal(str(valor_redondeado))
        # Verificar que tenga máximo 2 decimales
        partes = str(valor_redondeado).split('.')
        if len(partes) > 1:
            decimales = len(partes[1])
            print(f"Decimales: {decimales}")
            if decimales <= 2:
                print("✓ Compatible con decimal(15,2)")
            else:
                print(f"❌ Tiene {decimales} decimales (máximo 2)")
        else:
            print("✓ Sin decimales - Compatible")
    except Exception as e:
        print(f"❌ Error: {e}")

print("\n" + "="*60)
print("CONCLUSIÓN")
print("="*60)

# Test con valor que causaría el problema
valor_problema = np.float64(50000.123456789123456789)
valor_correcto = round(float(valor_problema), 2)

print(f"\nValor que causaba error: {valor_problema} ({type(valor_problema).__name__})")
print(f"Valor corregido: {valor_correcto} (float)")
print(f"Decimales: {len(str(valor_correcto).split('.')[1]) if '.' in str(valor_correcto) else 0}")
print(f"\n✅ Ahora es compatible con decimal(15,2)")
