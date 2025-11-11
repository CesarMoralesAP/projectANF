"""
Test rápido para verificar conversión de numpy a float
"""
import numpy as np

# Simular el array de numpy que se genera
valores_proj = np.array([50000.5, 52000.75, 53500.25])

print("Tipo original:", type(valores_proj[0]))
print("Valor original:", valores_proj[0])

# Convertir a float de Python
valores_convertidos = [float(v) for v in valores_proj]

print("\nTipo convertido:", type(valores_convertidos[0]))
print("Valor convertido:", valores_convertidos[0])

# Verificar que es decimal-compatible
from decimal import Decimal
try:
    d = Decimal(str(valores_convertidos[0]))
    print("\n✓ Conversión a Decimal exitosa:", d)
except Exception as e:
    print(f"\n❌ Error en conversión: {e}")
