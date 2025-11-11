"""
Script para verificar la agrupación de ratios por categoría.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.catalogos.models import RatioFinanciero

print("="*70)
print("VERIFICACIÓN DE CATEGORÍAS DE RATIOS")
print("="*70)

ratios = RatioFinanciero.objects.all().order_by('categoria', 'nombre')

# Agrupar por categoría
categorias = {}
for ratio in ratios:
    cat = ratio.categoria or 'Sin categoría'
    if cat not in categorias:
        categorias[cat] = []
    categorias[cat].append(ratio)

print(f"\n📊 Total de ratios: {ratios.count()}")
print(f"📂 Total de categorías: {len(categorias)}")

for categoria, ratios_lista in sorted(categorias.items()):
    print(f"\n{'='*70}")
    print(f"📁 {categoria.upper()} ({len(ratios_lista)} ratios)")
    print('='*70)
    
    for ratio in ratios_lista:
        componentes = ratio.componentes.count()
        print(f"   • {ratio.nombre}")
        print(f"     Fórmula: {ratio.formula_display}")
        print(f"     Componentes: {componentes}")
        if ratio.promedio_general:
            print(f"     Promedio general: {ratio.promedio_general}")
        print()

print("="*70)
print("✅ VERIFICACIÓN COMPLETADA")
print("="*70)
