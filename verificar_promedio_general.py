"""
Script para verificar el promedio general de los ratios.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.catalogos.models import RatioFinanciero

print("="*60)
print("VERIFICACIÓN DE PROMEDIO GENERAL EN RATIOS")
print("="*60)

ratios = RatioFinanciero.objects.all()

print(f"\n📊 Total de ratios: {ratios.count()}")

for ratio in ratios:
    pg = ratio.promedio_general
    status = "✅" if pg is not None else "❌"
    valor = f"{pg}" if pg is not None else "NULL"
    print(f"{status} {ratio.nombre}: {valor}")

# Contar cuántos tienen promedio_general
con_promedio = ratios.filter(promedio_general__isnull=False).count()
sin_promedio = ratios.filter(promedio_general__isnull=True).count()

print(f"\n📈 Resumen:")
print(f"   Con promedio general: {con_promedio}")
print(f"   Sin promedio general: {sin_promedio}")

print("\n" + "="*60)
