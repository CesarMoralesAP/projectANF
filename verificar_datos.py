"""
Script para verificar datos en la base de datos para el módulo de análisis.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.empresas.models import Empresa
from apps.catalogos.models import CatalogoCuenta, MapeoCuentaRatio
from apps.estados.models import EstadoFinanciero
from apps.catalogos.models import RatioFinanciero

print("="*60)
print("VERIFICACIÓN DE DATOS PARA MÓDULO DE ANÁLISIS")
print("="*60)

# Verificar empresas
empresas = Empresa.objects.all()
print(f"\n📊 Total de empresas: {empresas.count()}")

for empresa in empresas[:5]:
    print(f"\n  Empresa: {empresa.nombre}")
    
    # Verificar catálogo
    try:
        catalogo = empresa.catalogo_cuenta
        print(f"    ✅ Tiene catálogo: {catalogo.cuentas.count()} cuentas")
        
        # Verificar mapeos
        mapeos = MapeoCuentaRatio.objects.filter(catalogo_cuenta=catalogo).count()
        print(f"    📋 Mapeos configurados: {mapeos}")
    except CatalogoCuenta.DoesNotExist:
        print(f"    ❌ No tiene catálogo configurado")
    
    # Verificar estados financieros
    estados = EstadoFinanciero.objects.filter(empresa=empresa)
    if estados.exists():
        años = estados.values_list('año', flat=True).distinct().order_by('año')
        print(f"    📈 Estados financieros en años: {list(años)}")
        for año in años:
            bg = estados.filter(año=año, tipo='BALANCE_GENERAL').exists()
            er = estados.filter(año=año, tipo='ESTADO_RESULTADOS').exists()
            print(f"       {año}: BG={'✅' if bg else '❌'} ER={'✅' if er else '❌'}")
    else:
        print(f"    ❌ No tiene estados financieros")

# Verificar ratios financieros
print(f"\n💹 Total de ratios financieros: {RatioFinanciero.objects.count()}")
ratios = RatioFinanciero.objects.all()[:3]
for ratio in ratios:
    componentes = ratio.componentes.count()
    print(f"  - {ratio.nombre}: {componentes} componentes")

print("\n" + "="*60)
