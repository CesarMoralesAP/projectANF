"""
Script para probar la actualización automática de promedios generales.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.empresas.models import Empresa
from apps.analisis.servicios.calcular_ratios import CalculadoraRatios
from apps.catalogos.models import RatioFinanciero
from django.contrib.auth.models import User

print("="*60)
print("PRUEBA DE ACTUALIZACIÓN DE PROMEDIOS GENERALES")
print("="*60)

# Mostrar estado inicial
print("\n📊 ESTADO INICIAL - Promedios Generales:")
ratios = RatioFinanciero.objects.all()
for ratio in ratios:
    pg = ratio.promedio_general
    valor = f"{pg}" if pg is not None else "NULL"
    print(f"   {ratio.nombre}: {valor}")

# Obtener Banco Agrícola
empresa = Empresa.objects.get(nombre="Banco Agrícola")
años = [2022, 2023, 2024]
usuario = User.objects.first()

print(f"\n🔄 Recalculando ratios para {empresa.nombre}...")
print(f"   Años: {años}")

# Recalcular ratios (esto debería actualizar promedios generales)
resultado = CalculadoraRatios.calcular_ratios_por_años(empresa, años, usuario)

print(f"\n✅ Ratios calculados: {len(resultado['ratios'])}")

# Mostrar estado después de la actualización
print("\n📊 ESTADO DESPUÉS DE ACTUALIZACIÓN - Promedios Generales:")
ratios = RatioFinanciero.objects.all()
for ratio in ratios:
    pg = ratio.promedio_general
    if pg is not None:
        print(f"   ✅ {ratio.nombre}: {pg}")
    else:
        print(f"   ❌ {ratio.nombre}: NULL")

# Verificar que los promedios se están usando en los cálculos
print("\n📈 VERIFICACIÓN EN RESULTADOS:")
for ratio_data in resultado['ratios'][:3]:
    print(f"\n   {ratio_data['nombre']}:")
    print(f"      Promedio general: {ratio_data['promedio_general']}")
    print(f"      Promedio sector: {ratio_data['promedio_sector']}")
    print(f"      Parámetro sectorial: {ratio_data['parametro_sectorial']}")
    
    # Mostrar un año de ejemplo
    for año, valores in list(ratio_data['valores_por_año'].items())[:1]:
        if valores:
            print(f"      Ejemplo {año}: Valor={valores['valor']}")
            print(f"         Superior a prom. general: {'✅' if valores['superior_promedio_general'] else '❌'}")

print("\n" + "="*60)
print("✅ PRUEBA COMPLETADA")
print("="*60)
