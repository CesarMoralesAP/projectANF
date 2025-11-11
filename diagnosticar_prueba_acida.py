"""
Script para investigar por qué no se calcula Prueba Ácida.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.catalogos.models import RatioFinanciero, MapeoCuentaRatio, CatalogoCuenta
from apps.empresas.models import Empresa
from apps.estados.models import EstadoFinanciero, ItemEstadoFinanciero

print("="*70)
print("DIAGNÓSTICO: RATIO PRUEBA ÁCIDA")
print("="*70)

# Obtener el ratio
try:
    ratio = RatioFinanciero.objects.get(nombre="Prueba Ácida")
    print(f"\n✅ Ratio encontrado: {ratio.nombre}")
    print(f"   Fórmula: {ratio.formula_display}")
    print(f"   Categoría: {ratio.categoria}")
except RatioFinanciero.DoesNotExist:
    print("\n❌ Ratio 'Prueba Ácida' no encontrado")
    exit()

# Verificar componentes
componentes = ratio.componentes.all()
print(f"\n📋 Componentes del ratio: {componentes.count()}")
for i, comp in enumerate(componentes, 1):
    print(f"   {i}. {comp.nombre_componente}")

# Verificar mapeos para Banco Agrícola
empresa = Empresa.objects.get(nombre="Banco Agrícola")
catalogo = empresa.catalogo_cuenta

print(f"\n🏢 Verificando mapeos para: {empresa.nombre}")
print(f"   Catálogo ID: {catalogo.id}")

for comp in componentes:
    try:
        mapeo = MapeoCuentaRatio.objects.get(
            catalogo_cuenta=catalogo,
            componente_ratio=comp
        )
        if mapeo.cuenta_contable:
            print(f"\n   ✅ {comp.nombre_componente}:")
            print(f"      → Mapeado a: {mapeo.cuenta_contable.nombre}")
            print(f"         Código: {mapeo.cuenta_contable.codigo}")
            
            # Verificar si hay valores en estados financieros
            año = 2024
            items = ItemEstadoFinanciero.objects.filter(
                cuenta_contable=mapeo.cuenta_contable,
                estado_financiero__empresa=empresa,
                estado_financiero__año=año
            )
            
            if items.exists():
                item = items.first()
                print(f"         Valor {año}: ${item.monto}")
                print(f"         Tipo estado: {item.estado_financiero.tipo}")
            else:
                print(f"         ⚠️ Sin valor en {año}")
        else:
            print(f"\n   ⚠️ {comp.nombre_componente}:")
            print(f"      Mapeo existe pero sin cuenta asignada")
    except MapeoCuentaRatio.DoesNotExist:
        print(f"\n   ❌ {comp.nombre_componente}:")
        print(f"      No existe mapeo")

# Verificar estados financieros
print(f"\n📊 Estados financieros de {empresa.nombre}:")
estados = EstadoFinanciero.objects.filter(empresa=empresa).order_by('año')
for estado in estados:
    items_count = estado.items.count()
    print(f"   {estado.año} - {estado.tipo}: {items_count} ítems")

print("\n" + "="*70)
