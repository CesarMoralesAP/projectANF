"""
Script para generar una plantilla Excel de ejemplo para Proyección de Ventas.
Ejecutar: python generar_plantilla_ejemplo.py
"""

import pandas as pd
from datetime import datetime

# Datos de ejemplo para 12 meses
datos_ejemplo = {
    'Año': [2023] * 12,
    'Mes': list(range(1, 13)),
    'Valor': [
        50000.00,
        52000.00,
        51500.00,
        53000.00,
        54500.00,
        55000.00,
        56000.00,
        57500.00,
        58000.00,
        59000.00,
        60000.00,
        61000.00
    ]
}

# Crear DataFrame
df = pd.DataFrame(datos_ejemplo)

# Guardar a Excel
nombre_archivo = f'plantilla_ventas_ejemplo_{datetime.now().strftime("%Y%m%d")}.xlsx'
df.to_excel(nombre_archivo, index=False)

print(f"✓ Plantilla generada exitosamente: {nombre_archivo}")
print(f"  - {len(df)} filas de datos")
print(f"  - Columnas: {', '.join(df.columns.tolist())}")
print(f"\nPuedes usar este archivo para probar el módulo de proyecciones.")
