from django.core.management.base import BaseCommand
from django.db import transaction
from apps.empresas.models import Empresa, Sector
from apps.catalogos.models import CatalogoCuenta, CuentaContable, TipoCuenta


class Command(BaseCommand):
    """
    Comando para crear el catálogo de cuentas de Banco Agrícola.
    """
    help = 'Crea el catálogo de cuentas de Banco Agrícola con cuentas predefinidas'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('\n📊 Creando catálogo de Banco Agrícola...\n'))
        
        try:
            with transaction.atomic():
                # Obtener o crear el sector bancario
                sector_bancario, _ = Sector.objects.get_or_create(
                    nombre='Bancario',
                    defaults={}
                )
                self.stdout.write(self.style.SUCCESS(f'✓ Sector: {sector_bancario.nombre}'))
                
                # Obtener o crear Banco Agrícola
                banco_agricola, created = Empresa.objects.get_or_create(
                    nombre='Banco Agrícola',
                    defaults={'sector': sector_bancario}
                )
                
                if created:
                    self.stdout.write(self.style.SUCCESS(f'✓ Empresa creada: {banco_agricola.nombre}'))
                else:
                    self.stdout.write(self.style.WARNING(f'⚠ Empresa ya existe: {banco_agricola.nombre}'))
                
                # Crear o obtener el catálogo
                catalogo, created = CatalogoCuenta.objects.get_or_create(
                    empresa=banco_agricola,
                    defaults={}
                )
                
                if created:
                    self.stdout.write(self.style.SUCCESS(f'✓ Catálogo creado para {banco_agricola.nombre}'))
                else:
                    self.stdout.write(self.style.WARNING(f'⚠ Catálogo ya existe, se actualizarán las cuentas'))
                    # Eliminar cuentas existentes para reemplazarlas
                    catalogo.cuentas.all().delete()
                
                # Definir las cuentas del catálogo
                cuentas = [
                    # ACTIVOS
                    {'codigo': '1', 'nombre': 'Activo', 'tipo': TipoCuenta.ACTIVO},
                    {'codigo': '1.1', 'nombre': 'Activo Corriente', 'tipo': TipoCuenta.ACTIVO},
                    {'codigo': '1.1.01', 'nombre': 'Caja y Bancos', 'tipo': TipoCuenta.ACTIVO},
                    {'codigo': '1.1.02', 'nombre': 'Cuentas por cobrar comerciales', 'tipo': TipoCuenta.ACTIVO},
                    {'codigo': '1.1.03', 'nombre': 'Otras cuentas por cobrar', 'tipo': TipoCuenta.ACTIVO},
                    {'codigo': '1.1.04', 'nombre': 'Inventarios', 'tipo': TipoCuenta.ACTIVO},
                    {'codigo': '1.1.05', 'nombre': 'Gastos pagados por anticipado', 'tipo': TipoCuenta.ACTIVO},
                    
                    {'codigo': '1.2', 'nombre': 'Activo No Corriente', 'tipo': TipoCuenta.ACTIVO},
                    {'codigo': '1.2.01', 'nombre': 'Inversiones en Valores', 'tipo': TipoCuenta.ACTIVO},
                    {'codigo': '1.2.02', 'nombre': 'Activo Fijo Neto', 'tipo': TipoCuenta.ACTIVO},
                    {'codigo': '1.2.03', 'nombre': 'Cartera de Créditos', 'tipo': TipoCuenta.ACTIVO},
                    
                    {'codigo': '1.3', 'nombre': 'Total Activo', 'tipo': TipoCuenta.ACTIVO},
                    
                    # PASIVOS
                    {'codigo': '2', 'nombre': 'Pasivo', 'tipo': TipoCuenta.PASIVO},
                    {'codigo': '2.1', 'nombre': 'Pasivo Corriente', 'tipo': TipoCuenta.PASIVO},
                    {'codigo': '2.1.01', 'nombre': 'Sobregiros y préstamos bancarios', 'tipo': TipoCuenta.PASIVO},
                    {'codigo': '2.1.02', 'nombre': 'Cuentas por pagar comerciales', 'tipo': TipoCuenta.PASIVO},
                    {'codigo': '2.1.03', 'nombre': 'Otras cuentas por pagar', 'tipo': TipoCuenta.PASIVO},
                    {'codigo': '2.1.04', 'nombre': 'Parte corriente deuda largo plazo', 'tipo': TipoCuenta.PASIVO},
                    {'codigo': '2.1.05', 'nombre': 'Depósitos de Clientes', 'tipo': TipoCuenta.PASIVO},
                    
                    {'codigo': '2.2', 'nombre': 'Pasivo No Corriente', 'tipo': TipoCuenta.PASIVO},
                    {'codigo': '2.2.01', 'nombre': 'Provisión CTS', 'tipo': TipoCuenta.PASIVO},
                    {'codigo': '2.2.02', 'nombre': 'Deuda a largo plazo', 'tipo': TipoCuenta.PASIVO},
                    {'codigo': '2.2.03', 'nombre': 'Obligaciones Financieras', 'tipo': TipoCuenta.PASIVO},
                    
                    {'codigo': '2.3', 'nombre': 'Total Pasivo', 'tipo': TipoCuenta.PASIVO},
                    
                    # PATRIMONIO
                    {'codigo': '3', 'nombre': 'Patrimonio', 'tipo': TipoCuenta.PATRIMONIO},
                    {'codigo': '3.1', 'nombre': 'Capital Social', 'tipo': TipoCuenta.PATRIMONIO},
                    {'codigo': '3.2', 'nombre': 'Resultados Acumulados', 'tipo': TipoCuenta.PATRIMONIO},
                    {'codigo': '3.3', 'nombre': 'Reservas', 'tipo': TipoCuenta.PATRIMONIO},
                    {'codigo': '3.4', 'nombre': 'Total Patrimonio', 'tipo': TipoCuenta.PATRIMONIO},
                    
                    # INGRESOS (para Estado de Resultados)
                    {'codigo': '4', 'nombre': 'Ingresos', 'tipo': TipoCuenta.INGRESO},
                    {'codigo': '4.1', 'nombre': 'Ingresos Financieros', 'tipo': TipoCuenta.INGRESO},
                    {'codigo': '4.1.01', 'nombre': 'Intereses por Préstamos', 'tipo': TipoCuenta.INGRESO},
                    {'codigo': '4.1.02', 'nombre': 'Comisiones por Servicios', 'tipo': TipoCuenta.INGRESO},
                    {'codigo': '4.2', 'nombre': 'Otros Ingresos', 'tipo': TipoCuenta.INGRESO},
                    {'codigo': '4.3', 'nombre': 'Total Ingresos', 'tipo': TipoCuenta.INGRESO},
                    
                    # GASTOS (para Estado de Resultados)
                    {'codigo': '5', 'nombre': 'Gastos', 'tipo': TipoCuenta.GASTO},
                    {'codigo': '5.1', 'nombre': 'Gastos Operativos', 'tipo': TipoCuenta.GASTO},
                    {'codigo': '5.1.01', 'nombre': 'Gastos de Personal', 'tipo': TipoCuenta.GASTO},
                    {'codigo': '5.1.02', 'nombre': 'Gastos Administrativos', 'tipo': TipoCuenta.GASTO},
                    {'codigo': '5.1.03', 'nombre': 'Depreciación', 'tipo': TipoCuenta.GASTO},
                    {'codigo': '5.2', 'nombre': 'Gastos Financieros', 'tipo': TipoCuenta.GASTO},
                    {'codigo': '5.2.01', 'nombre': 'Intereses por Obligaciones', 'tipo': TipoCuenta.GASTO},
                    {'codigo': '5.3', 'nombre': 'Provisiones', 'tipo': TipoCuenta.GASTO},
                    {'codigo': '5.3.01', 'nombre': 'Provisión para Créditos Incobrables', 'tipo': TipoCuenta.GASTO},
                    {'codigo': '5.4', 'nombre': 'Total Gastos', 'tipo': TipoCuenta.GASTO},
                    
                    # RESULTADOS
                    {'codigo': '6', 'nombre': 'Resultados', 'tipo': TipoCuenta.RESULTADO},
                    {'codigo': '6.1', 'nombre': 'Utilidad Operativa', 'tipo': TipoCuenta.RESULTADO},
                    {'codigo': '6.2', 'nombre': 'Utilidad antes de Impuestos', 'tipo': TipoCuenta.RESULTADO},
                    {'codigo': '6.3', 'nombre': 'Impuesto a la Renta', 'tipo': TipoCuenta.GASTO},
                    {'codigo': '6.4', 'nombre': 'Utilidad Neta', 'tipo': TipoCuenta.RESULTADO},
                ]
                
                # Crear las cuentas
                cuentas_creadas = 0
                for cuenta_data in cuentas:
                    cuenta = CuentaContable.objects.create(
                        catalogo=catalogo,
                        codigo=cuenta_data['codigo'],
                        nombre=cuenta_data['nombre'],
                        tipo=cuenta_data['tipo']
                    )
                    cuentas_creadas += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'  ✓ {cuenta.codigo} - {cuenta.nombre}')
                    )
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f'\n✓ Catálogo completado: {cuentas_creadas} cuentas creadas para {banco_agricola.nombre}'
                    )
                )
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'\n✗ Error: {str(e)}'))
            raise
