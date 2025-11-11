from django.core.management.base import BaseCommand
from django.db import transaction
from apps.empresas.models import Empresa
from apps.catalogos.models import (
    CatalogoCuenta, 
    CuentaContable, 
    RatioFinanciero, 
    ComponenteRatio, 
    MapeoCuentaRatio
)


class Command(BaseCommand):
    """
    Comando para crear los mapeos de cuentas contables a componentes de ratios
    para Banco Agrícola.
    """
    help = 'Crea los mapeos de ratios financieros para Banco Agrícola'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('\n📊 Creando mapeos de ratios para Banco Agrícola...\n'))
        
        try:
            with transaction.atomic():
                # Obtener Banco Agrícola
                try:
                    banco_agricola = Empresa.objects.get(nombre='Banco Agrícola')
                except Empresa.DoesNotExist:
                    self.stdout.write(
                        self.style.ERROR('✗ Error: Banco Agrícola no existe. Ejecuta primero crear_catalogo_banco_agricola')
                    )
                    return
                
                # Obtener catálogo
                try:
                    catalogo = CatalogoCuenta.objects.get(empresa=banco_agricola)
                except CatalogoCuenta.DoesNotExist:
                    self.stdout.write(
                        self.style.ERROR('✗ Error: Catálogo no existe. Ejecuta primero crear_catalogo_banco_agricola')
                    )
                    return
                
                # Obtener las cuentas del catálogo
                cuentas = {
                    cuenta.codigo: cuenta 
                    for cuenta in CuentaContable.objects.filter(catalogo=catalogo)
                }
                
                # Verificar que existen los ratios
                if not RatioFinanciero.objects.exists():
                    self.stdout.write(
                        self.style.WARNING('⚠ No hay ratios financieros. Ejecuta primero crear_ratios_demo')
                    )
                    return
                
                # Eliminar mapeos existentes
                MapeoCuentaRatio.objects.filter(catalogo_cuenta=catalogo).delete()
                self.stdout.write(self.style.WARNING('⚠ Mapeos anteriores eliminados\n'))
                
                # Definir los mapeos
                # Formato: (nombre_ratio, nombre_componente, codigo_cuenta)
                mapeos_definicion = [
                    # RAZÓN CORRIENTE = Activo Corriente / Pasivo Corriente
                    ('Razón Corriente', 'Activo Corriente', '1.1'),
                    ('Razón Corriente', 'Pasivo Corriente', '2.1'),
                    
                    # PRUEBA ÁCIDA = (Activo Corriente - Inventario) / Pasivo Corriente
                    ('Prueba Ácida', 'Activo Corriente', '1.1'),
                    ('Prueba Ácida', 'Inventario', '1.1.04'),
                    ('Prueba Ácida', 'Pasivo Corriente', '2.1'),
                    
                    # RATIO DE ENDEUDAMIENTO = Pasivo Total / Patrimonio Total
                    ('Ratio de Endeudamiento', 'Pasivo Total', '2.3'),
                    ('Ratio de Endeudamiento', 'Patrimonio Total', '3.4'),
                    
                    # COBERTURA DE INTERESES = Utilidad Operativa / Gastos Financieros
                    ('Cobertura de Intereses', 'Utilidad Operativa', '6.1'),
                    ('Cobertura de Intereses', 'Gastos Financieros', '5.2'),
                    
                    # ROE = (Utilidad Neta / Patrimonio) × 100
                    ('ROE', 'Utilidad Neta', '6.4'),
                    ('ROE', 'Patrimonio', '3.4'),
                    
                    # ROA = (Utilidad Neta / Activo Total) × 100
                    ('ROA', 'Utilidad Neta', '6.4'),
                    ('ROA', 'Activo Total', '1.3'),
                ]
                
                mapeos_creados = 0
                mapeos_por_ratio = {}
                
                for nombre_ratio, nombre_componente, codigo_cuenta in mapeos_definicion:
                    try:
                        # Buscar el ratio
                        ratio = RatioFinanciero.objects.get(nombre=nombre_ratio)
                        
                        # Buscar el componente
                        componente = ComponenteRatio.objects.get(
                            ratio_financiero=ratio,
                            nombre_componente=nombre_componente
                        )
                        
                        # Buscar la cuenta
                        if codigo_cuenta not in cuentas:
                            self.stdout.write(
                                self.style.ERROR(
                                    f'  ✗ Cuenta {codigo_cuenta} no encontrada para {nombre_componente}'
                                )
                            )
                            continue
                        
                        cuenta = cuentas[codigo_cuenta]
                        
                        # Crear el mapeo
                        mapeo = MapeoCuentaRatio.objects.create(
                            catalogo_cuenta=catalogo,
                            componente_ratio=componente,
                            cuenta_contable=cuenta
                        )
                        
                        mapeos_creados += 1
                        
                        # Agrupar por ratio para el resumen
                        if nombre_ratio not in mapeos_por_ratio:
                            mapeos_por_ratio[nombre_ratio] = []
                        mapeos_por_ratio[nombre_ratio].append(
                            f'{nombre_componente} → {cuenta.codigo} ({cuenta.nombre})'
                        )
                        
                    except RatioFinanciero.DoesNotExist:
                        self.stdout.write(
                            self.style.ERROR(f'  ✗ Ratio "{nombre_ratio}" no encontrado')
                        )
                    except ComponenteRatio.DoesNotExist:
                        self.stdout.write(
                            self.style.ERROR(
                                f'  ✗ Componente "{nombre_componente}" no encontrado para ratio "{nombre_ratio}"'
                            )
                        )
                    except Exception as e:
                        self.stdout.write(
                            self.style.ERROR(f'  ✗ Error creando mapeo: {str(e)}')
                        )
                
                # Mostrar resumen por ratio
                self.stdout.write(self.style.SUCCESS('\n📊 Resumen de mapeos creados:\n'))
                for nombre_ratio, mapeos in mapeos_por_ratio.items():
                    self.stdout.write(self.style.SUCCESS(f'\n{nombre_ratio}:'))
                    for mapeo in mapeos:
                        self.stdout.write(self.style.SUCCESS(f'  ✓ {mapeo}'))
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f'\n✓ Total de mapeos creados: {mapeos_creados}'
                    )
                )
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'\n✗ Error: {str(e)}'))
            import traceback
            self.stdout.write(self.style.ERROR(traceback.format_exc()))
            raise
