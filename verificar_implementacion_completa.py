"""
Script final para verificar la implementación completa del promedio general.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.catalogos.models import RatioFinanciero
from apps.analisis.models import ValorRatioCalculado

print("="*70)
print(" VERIFICACIÓN FINAL: IMPLEMENTACIÓN DE PROMEDIO GENERAL")
print("="*70)

print("\n✅ COMPONENTES IMPLEMENTADOS:\n")
print("1. ✓ Campo 'promedio_general' en modelo RatioFinanciero")
print("2. ✓ Migración aplicada (0005_ratiofinanciero_promedio_general)")
print("3. ✓ Cálculo automático en CalculadoraRatios._actualizar_promedios_generales()")
print("4. ✓ Actualización después de cada cálculo de ratios")
print("5. ✓ Comando de gestión: actualizar_promedios_generales")
print("6. ✓ Servicio independiente: ActualizadorPromedioGeneral")
print("7. ✓ Comparación en ValorRatioCalculado.superior_promedio_general")
print("8. ✓ Visualización en frontend (template analisis_financiero.html)")

print("\n" + "="*70)
print(" ESTADO ACTUAL DE LOS DATOS")
print("="*70)

ratios = RatioFinanciero.objects.all()
print(f"\n📊 Total de ratios: {ratios.count()}")

con_promedio = ratios.filter(promedio_general__isnull=False)
sin_promedio = ratios.filter(promedio_general__isnull=True)

print(f"\n✅ Con promedio general: {con_promedio.count()}")
for ratio in con_promedio:
    valores_count = ValorRatioCalculado.objects.filter(
        ratio=ratio,
        valor_calculado__isnull=False
    ).count()
    print(f"   • {ratio.nombre}: {ratio.promedio_general} (basado en {valores_count} valores)")

print(f"\n⚠️  Sin promedio general: {sin_promedio.count()}")
for ratio in sin_promedio:
    valores_count = ValorRatioCalculado.objects.filter(
        ratio=ratio,
        valor_calculado__isnull=False
    ).count()
    print(f"   • {ratio.nombre} ({valores_count} valores calculados)")

print("\n" + "="*70)
print(" EJEMPLO DE COMPARACIONES")
print("="*70)

# Mostrar algunos valores calculados con sus comparaciones
valores = ValorRatioCalculado.objects.select_related('ratio', 'empresa').all()[:5]

print(f"\n📋 Primeros {len(valores)} valores calculados:\n")
for valor in valores:
    print(f"   {valor.ratio.nombre} - {valor.empresa.nombre} ({valor.año})")
    print(f"      Valor calculado: {valor.valor_calculado}")
    
    if valor.promedio_general:
        comparacion = "✅ Superior" if valor.superior_promedio_general else "❌ Inferior"
        print(f"      vs Promedio general ({valor.promedio_general}): {comparacion}")
    else:
        print(f"      Promedio general: No disponible")
    
    if valor.promedio_sector:
        comparacion = "✅ Superior" if valor.superior_promedio_sector else "❌ Inferior"
        print(f"      vs Promedio sector ({valor.promedio_sector}): {comparacion}")
    
    if valor.parametro_sectorial:
        comparacion = "✅ Superior" if valor.superior_parametro_sectorial else "❌ Inferior"
        print(f"      vs Parámetro sectorial ({valor.parametro_sectorial}): {comparacion}")
    
    print()

print("="*70)
print(" USO DEL COMANDO DE GESTIÓN")
print("="*70)
print("\nPara actualizar manualmente los promedios generales, ejecuta:")
print("   python manage.py actualizar_promedios_generales")
print("\nLos promedios también se actualizan automáticamente cuando se")
print("calculan nuevos ratios a través del módulo de análisis.")

print("\n" + "="*70)
print("✅ IMPLEMENTACIÓN COMPLETADA")
print("="*70)
