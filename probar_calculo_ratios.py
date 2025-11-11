"""
Script para probar el cálculo de ratios financieros.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.empresas.models import Empresa
from apps.analisis.servicios.calcular_ratios import CalculadoraRatios
from apps.analisis.models import ValorRatioCalculado
from django.contrib.auth.models import User

print("="*60)
print("PRUEBA DE CÁLCULO DE RATIOS FINANCIEROS")
print("="*60)

# Obtener Banco Agrícola
empresa = Empresa.objects.get(nombre="Banco Agrícola")
print(f"\n🏢 Empresa: {empresa.nombre}")
print(f"   Sector: {empresa.sector.nombre}")

# Años a calcular
años = [2022, 2023, 2024]
print(f"\n📅 Años a calcular: {años}")

# Obtener usuario (para el audit trail)
try:
    usuario = User.objects.first()
    print(f"👤 Usuario: {usuario.username}")
except:
    usuario = None
    print(f"👤 Usuario: Sin usuario (modo prueba)")

print("\n🔄 Calculando ratios...")

# Calcular ratios
resultado = CalculadoraRatios.calcular_ratios_por_años(empresa, años, usuario)

if 'error' in resultado:
    print(f"\n❌ Error: {resultado['error']}")
else:
    ratios = resultado['ratios']
    print(f"\n✅ Ratios calculados: {len(ratios)}")
    
    for ratio in ratios[:3]:  # Mostrar primeros 3
        print(f"\n  📊 {ratio['nombre']} ({ratio['categoria']})")
        print(f"     Fórmula: {ratio['formula']}")
        if ratio['parametro_sectorial']:
            print(f"     Parámetro sectorial: {ratio['parametro_sectorial']}")
        if ratio['promedio_sector']:
            print(f"     Promedio sector: {ratio['promedio_sector']}")
        if ratio['promedio_general']:
            print(f"     Promedio general: {ratio['promedio_general']}")
        
        for año, valor_data in ratio['valores_por_año'].items():
            if valor_data:
                valor = valor_data['valor']
                print(f"     {año}: {valor}", end="")
                
                if valor_data['superior_parametro']:
                    print(" ✅ > Parámetro", end="")
                if valor_data['superior_promedio_sector']:
                    print(" ✅ > Prom. Sector", end="")
                if valor_data['superior_promedio_general']:
                    print(" ✅ > Prom. General", end="")
                print()
            else:
                print(f"     {año}: No calculable")

# Verificar que se guardaron en la base de datos
print("\n" + "="*60)
print("VERIFICACIÓN EN BASE DE DATOS")
print("="*60)

valores_guardados = ValorRatioCalculado.objects.filter(
    empresa=empresa,
    año__in=años
)

print(f"\n💾 Valores guardados en BD: {valores_guardados.count()}")

# Agrupar por año
for año in años:
    count = valores_guardados.filter(año=año).count()
    print(f"   {año}: {count} ratios")

# Mostrar algunos valores guardados
print(f"\n📋 Primeros 3 valores guardados:")
for valor in valores_guardados[:3]:
    print(f"   - {valor.ratio.nombre} ({valor.año}): {valor.valor_calculado}")
    print(f"     Usuario: {valor.usuario_calculo.username if valor.usuario_calculo else 'N/A'}")
    print(f"     Fecha: {valor.fecha_calculo.strftime('%Y-%m-%d %H:%M')}")
    print(f"     Superior a parámetro sectorial: {'✅' if valor.superior_parametro_sectorial else '❌'}")

print("\n" + "="*60)
print("✅ PRUEBA COMPLETADA")
print("="*60)
