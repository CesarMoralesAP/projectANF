"""
Script para probar el cálculo del ratio Prueba Ácida.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.empresas.models import Empresa
from apps.analisis.servicios.calcular_ratios import CalculadoraRatios
from apps.catalogos.models import RatioFinanciero
from apps.analisis.models import ValorRatioCalculado
from django.contrib.auth.models import User

print("="*70)
print("PRUEBA: CÁLCULO DE RATIO PRUEBA ÁCIDA")
print("="*70)

# Obtener Banco Agrícola
empresa = Empresa.objects.get(nombre="Banco Agrícola")
años = [2022, 2023, 2024]
usuario = User.objects.first()

print(f"\n🏢 Empresa: {empresa.nombre}")
print(f"📅 Años: {años}")

# Mostrar valores de las cuentas para 2024
from apps.estados.models import EstadoFinanciero, ItemEstadoFinanciero
año_ejemplo = 2024
estado = EstadoFinanciero.objects.get(empresa=empresa, año=año_ejemplo, tipo='BALANCE_GENERAL')

print(f"\n💰 Valores para el año {año_ejemplo}:")
cuentas_prueba = ['1.1', '1.1.04', '2.1']  # Activo Corriente, Inventarios, Pasivo Corriente
for codigo in cuentas_prueba:
    try:
        item = ItemEstadoFinanciero.objects.get(
            estado_financiero=estado,
            cuenta_contable__codigo=codigo
        )
        print(f"   {item.cuenta_contable.nombre} ({codigo}): ${item.monto:,.2f}")
    except:
        print(f"   Cuenta {codigo}: No encontrada")

# Calcular manualmente para verificar
print(f"\n🧮 Cálculo manual de Prueba Ácida {año_ejemplo}:")
activo = 2845000
inventario = 210000
pasivo = 11370000
resultado_manual = (activo - inventario) / pasivo
print(f"   ({activo:,} - {inventario:,}) / {pasivo:,} = {resultado_manual:.4f}")

# Ejecutar el cálculo automático
print(f"\n🔄 Ejecutando cálculo automático...")
resultado = CalculadoraRatios.calcular_ratios_por_años(empresa, años, usuario)

if 'error' in resultado:
    print(f"\n❌ Error: {resultado['error']}")
else:
    ratios = resultado['ratios']
    print(f"\n✅ Total de ratios calculados: {len(ratios)}")
    
    # Buscar Prueba Ácida
    prueba_acida = None
    for ratio in ratios:
        if ratio['nombre'] == 'Prueba Ácida':
            prueba_acida = ratio
            break
    
    if prueba_acida:
        print(f"\n✅ PRUEBA ÁCIDA CALCULADA:")
        print(f"   Fórmula: {prueba_acida['formula']}")
        print(f"   Categoría: {prueba_acida['categoria']}")
        
        for año, valores in prueba_acida['valores_por_año'].items():
            if valores:
                print(f"\n   Año {año}:")
                print(f"      Valor calculado: {valores['valor']}")
                if prueba_acida['parametro_sectorial']:
                    comparacion = "✅" if valores['superior_parametro'] else "❌"
                    print(f"      vs Parámetro sectorial ({prueba_acida['parametro_sectorial']}): {comparacion}")
                if prueba_acida['promedio_sector']:
                    comparacion = "✅" if valores['superior_promedio_sector'] else "❌"
                    print(f"      vs Promedio sector ({prueba_acida['promedio_sector']}): {comparacion}")
                if prueba_acida['promedio_general']:
                    comparacion = "✅" if valores['superior_promedio_general'] else "❌"
                    print(f"      vs Promedio general ({prueba_acida['promedio_general']}): {comparacion}")
    else:
        print(f"\n❌ Prueba Ácida NO fue calculada")

# Verificar en la base de datos
print(f"\n💾 Verificación en Base de Datos:")
ratio_obj = RatioFinanciero.objects.get(nombre="Prueba Ácida")
valores_bd = ValorRatioCalculado.objects.filter(
    empresa=empresa,
    ratio=ratio_obj,
    año__in=años
).order_by('año')

if valores_bd.exists():
    print(f"   ✅ {valores_bd.count()} valores guardados para Prueba Ácida:")
    for valor in valores_bd:
        print(f"      {valor.año}: {valor.valor_calculado}")
else:
    print(f"   ❌ No hay valores guardados para Prueba Ácida")

# Actualizar promedio general
print(f"\n📊 Promedio General de Prueba Ácida:")
ratio_obj_actualizado = RatioFinanciero.objects.get(nombre="Prueba Ácida")
if ratio_obj_actualizado.promedio_general:
    print(f"   ✅ Promedio general: {ratio_obj_actualizado.promedio_general}")
else:
    print(f"   ⚠️ Sin promedio general")

print("\n" + "="*70)
print("✅ PRUEBA COMPLETADA")
print("="*70)
