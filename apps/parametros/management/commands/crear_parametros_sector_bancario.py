from django.core.management.base import BaseCommand
from django.db import transaction
from apps.empresas.models import Sector
from apps.catalogos.models import RatioFinanciero
from apps.parametros.models import RatioReferenciaSector


class Command(BaseCommand):
    """
    Comando para crear los parámetros de referencia del sector bancario.
    Asigna valores óptimos para cada ratio financiero según estándares del sector bancario.
    """
    help = 'Crea los parámetros de referencia (valores óptimos) para el sector bancario'

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('\n📊 Creando parámetros de referencia para el sector bancario...\n')
        )
        
        try:
            with transaction.atomic():
                # Obtener o crear el sector bancario
                sector_bancario, created = Sector.objects.get_or_create(
                    nombre='Bancario',
                    defaults={}
                )
                
                if created:
                    self.stdout.write(self.style.SUCCESS(f'✓ Sector creado: {sector_bancario.nombre}'))
                else:
                    self.stdout.write(self.style.WARNING(f'⚠ Sector ya existe: {sector_bancario.nombre}'))
                
                # Verificar que existen ratios financieros
                if not RatioFinanciero.objects.exists():
                    self.stdout.write(
                        self.style.ERROR(
                            '✗ Error: No hay ratios financieros. Ejecuta primero crear_ratios_demo'
                        )
                    )
                    return
                
                # Eliminar parámetros anteriores del sector bancario
                eliminados = RatioReferenciaSector.objects.filter(sector=sector_bancario).delete()[0]
                if eliminados > 0:
                    self.stdout.write(
                        self.style.WARNING(f'⚠ {eliminados} parámetros anteriores eliminados\n')
                    )
                
                # Definir los valores óptimos para el sector bancario
                # Basados en estándares internacionales y mejores prácticas del sector financiero
                parametros_definicion = {
                    # === RATIOS DE LIQUIDEZ ===
                    'Razón Corriente': {
                        'valor_optimo': 1.20,  # Bancos suelen mantener menor liquidez que otros sectores
                        'descripcion': 'Capacidad de pago de obligaciones a corto plazo'
                    },
                    'Prueba Ácida': {
                        'valor_optimo': 1.00,  # Similar a razón corriente pero sin inventarios
                        'descripcion': 'Liquidez sin considerar inventarios'
                    },
                    
                    # === RATIOS DE ENDEUDAMIENTO ===
                    'Ratio de Endeudamiento Total': {
                        'valor_optimo': 0.90,  # Los bancos son altamente apalancados (90% pasivos)
                        'descripcion': 'Proporción de activos financiados con deuda'
                    },
                    'Ratio de Autonomía Financiera': {
                        'valor_optimo': 0.10,  # 10% de capital propio (complemento del endeudamiento)
                        'descripcion': 'Proporción de activos financiados con capital propio'
                    },
                    
                    # === RATIOS DE RENTABILIDAD ===
                    'ROA': {
                        'valor_optimo': 1.50,  # 1.5% es un ROA saludable para bancos
                        'descripcion': 'Rentabilidad sobre activos totales'
                    },
                    'ROE': {
                        'valor_optimo': 15.00,  # 15% es un ROE bueno para bancos
                        'descripcion': 'Rentabilidad sobre patrimonio'
                    },
                    'Margen Neto': {
                        'valor_optimo': 25.00,  # 25% de margen neto es saludable
                        'descripcion': 'Utilidad neta como porcentaje de ingresos'
                    },
                    'Margen de Interés Neto (NIM)': {
                        'valor_optimo': 4.50,  # 4.5% es un NIM típico para bancos
                        'descripcion': 'Diferencial entre ingresos y gastos financieros sobre activos productivos'
                    },
                    'Margen Operativo': {
                        'valor_optimo': 40.00,  # 40% de margen operativo es bueno
                        'descripcion': 'Eficiencia operativa antes de impuestos'
                    },
                    
                    # === RATIOS DE EFICIENCIA ===
                    'Ratio de Eficiencia': {
                        'valor_optimo': 55.00,  # 55% o menos es eficiente (menor es mejor)
                        'descripcion': 'Gastos operativos como porcentaje del margen bruto'
                    },
                }
                
                parametros_creados = 0
                parametros_por_categoria = {}
                
                for nombre_ratio, datos in parametros_definicion.items():
                    try:
                        # Buscar el ratio
                        ratio = RatioFinanciero.objects.get(nombre=nombre_ratio)
                        
                        # Crear el parámetro de referencia
                        parametro = RatioReferenciaSector.objects.create(
                            ratio_financiero=ratio,
                            sector=sector_bancario,
                            valor_optimo=datos['valor_optimo'],
                            promedio_sector=None  # Se calculará después con datos reales
                        )
                        
                        parametros_creados += 1
                        
                        # Agrupar por categoría para el resumen
                        categoria = ratio.categoria
                        if categoria not in parametros_por_categoria:
                            parametros_por_categoria[categoria] = []
                        
                        parametros_por_categoria[categoria].append({
                            'nombre': nombre_ratio,
                            'valor': datos['valor_optimo'],
                            'descripcion': datos['descripcion']
                        })
                        
                    except RatioFinanciero.DoesNotExist:
                        self.stdout.write(
                            self.style.ERROR(f'  ✗ Ratio "{nombre_ratio}" no encontrado')
                        )
                    except Exception as e:
                        self.stdout.write(
                            self.style.ERROR(f'  ✗ Error creando parámetro para "{nombre_ratio}": {str(e)}')
                        )
                
                # Mostrar resumen por categoría
                self.stdout.write(
                    self.style.SUCCESS(
                        '\n📊 Parámetros de referencia creados por categoría:\n'
                    )
                )
                
                # Definir orden de categorías
                orden_categorias = ['Liquidez', 'Endeudamiento', 'Rentabilidad', 'Eficiencia']
                
                for categoria in orden_categorias:
                    if categoria in parametros_por_categoria:
                        self.stdout.write(self.style.SUCCESS(f'\n💧 {categoria.upper()}:'))
                        parametros = parametros_por_categoria[categoria]
                        for param in parametros:
                            self.stdout.write(
                                self.style.SUCCESS(
                                    f'  ✓ {param["nombre"]}: {param["valor"]}%'
                                    if categoria != 'Liquidez' and categoria != 'Endeudamiento'
                                    else f'  ✓ {param["nombre"]}: {param["valor"]}'
                                )
                            )
                            self.stdout.write(
                                self.style.HTTP_INFO(f'    └─ {param["descripcion"]}')
                            )
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f'\n✓ Total de parámetros creados: {parametros_creados} para el sector {sector_bancario.nombre}'
                    )
                )
                
                self.stdout.write(
                    self.style.HTTP_INFO(
                        '\n💡 Nota: Los valores de "Promedio del Sector" se calcularán automáticamente '
                        'cuando existan datos de múltiples empresas del sector.\n'
                    )
                )
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'\n✗ Error: {str(e)}'))
            import traceback
            self.stdout.write(self.style.ERROR(traceback.format_exc()))
            raise
