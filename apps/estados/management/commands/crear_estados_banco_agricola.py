from django.core.management.base import BaseCommand
from django.db import transaction
from decimal import Decimal
from apps.empresas.models import Empresa
from apps.catalogos.models import CatalogoCuenta, CuentaContable
from apps.estados.models import EstadoFinanciero, ItemEstadoFinanciero, TipoEstadoFinanciero


class Command(BaseCommand):
    """
    Comando para crear estados financieros de demostración para Banco Agrícola.
    Crea 3 Balances Generales y 3 Estados de Resultados (años 2022, 2023, 2024).
    """
    help = 'Crea estados financieros de demostración para Banco Agrícola'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('\n📊 Creando estados financieros de Banco Agrícola...\n'))
        
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
                
                # Definir los años
                años = [2022, 2023, 2024]
                
                # Crear Balances Generales
                self.stdout.write(self.style.SUCCESS('\n📋 Creando Balances Generales...\n'))
                
                datos_balances = {
                    2022: {
                        # ACTIVOS
                        '1.1.01': Decimal('450000.00'),    # Caja y Bancos
                        '1.1.02': Decimal('1200000.00'),   # Cuentas por cobrar comerciales
                        '1.1.03': Decimal('350000.00'),    # Otras cuentas por cobrar
                        '1.1.04': Decimal('180000.00'),    # Inventarios
                        '1.1.05': Decimal('75000.00'),     # Gastos pagados por anticipado
                        '1.1': Decimal('2255000.00'),      # Activo Corriente
                        
                        '1.2.01': Decimal('850000.00'),    # Inversiones en Valores
                        '1.2.02': Decimal('1500000.00'),   # Activo Fijo Neto
                        '1.2.03': Decimal('8500000.00'),   # Cartera de Créditos
                        '1.2': Decimal('10850000.00'),     # Activo No Corriente
                        
                        '1.3': Decimal('13105000.00'),     # Total Activo
                        
                        # PASIVOS
                        '2.1.01': Decimal('500000.00'),    # Sobregiros y préstamos bancarios
                        '2.1.02': Decimal('320000.00'),    # Cuentas por pagar comerciales
                        '2.1.03': Decimal('180000.00'),    # Otras cuentas por pagar
                        '2.1.04': Decimal('250000.00'),    # Parte corriente deuda largo plazo
                        '2.1.05': Decimal('7500000.00'),   # Depósitos de Clientes
                        '2.1': Decimal('8750000.00'),      # Pasivo Corriente
                        
                        '2.2.01': Decimal('120000.00'),    # Provisión CTS
                        '2.2.02': Decimal('1200000.00'),   # Deuda a largo plazo
                        '2.2.03': Decimal('1500000.00'),   # Obligaciones Financieras
                        '2.2': Decimal('2820000.00'),      # Pasivo No Corriente
                        
                        '2.3': Decimal('11570000.00'),     # Total Pasivo
                        
                        # PATRIMONIO
                        '3.1': Decimal('1000000.00'),      # Capital Social
                        '3.2': Decimal('385000.00'),       # Resultados Acumulados
                        '3.3': Decimal('150000.00'),       # Reservas
                        '3.4': Decimal('1535000.00'),      # Total Patrimonio
                    },
                    2023: {
                        # ACTIVOS
                        '1.1.01': Decimal('520000.00'),    
                        '1.1.02': Decimal('1350000.00'),   
                        '1.1.03': Decimal('400000.00'),    
                        '1.1.04': Decimal('195000.00'),    
                        '1.1.05': Decimal('85000.00'),     
                        '1.1': Decimal('2550000.00'),      
                        
                        '1.2.01': Decimal('950000.00'),    
                        '1.2.02': Decimal('1650000.00'),   
                        '1.2.03': Decimal('9800000.00'),   
                        '1.2': Decimal('12400000.00'),     
                        
                        '1.3': Decimal('14950000.00'),     
                        
                        # PASIVOS
                        '2.1.01': Decimal('550000.00'),    
                        '2.1.02': Decimal('380000.00'),    
                        '2.1.03': Decimal('210000.00'),    
                        '2.1.04': Decimal('280000.00'),    
                        '2.1.05': Decimal('8600000.00'),   
                        '2.1': Decimal('10020000.00'),     
                        
                        '2.2.01': Decimal('135000.00'),    
                        '2.2.02': Decimal('1350000.00'),   
                        '2.2.03': Decimal('1650000.00'),   
                        '2.2': Decimal('3135000.00'),      
                        
                        '2.3': Decimal('13155000.00'),     
                        
                        # PATRIMONIO
                        '3.1': Decimal('1000000.00'),      
                        '3.2': Decimal('600000.00'),       
                        '3.3': Decimal('195000.00'),       
                        '3.4': Decimal('1795000.00'),      
                    },
                    2024: {
                        # ACTIVOS
                        '1.1.01': Decimal('610000.00'),    
                        '1.1.02': Decimal('1480000.00'),   
                        '1.1.03': Decimal('450000.00'),    
                        '1.1.04': Decimal('210000.00'),    
                        '1.1.05': Decimal('95000.00'),     
                        '1.1': Decimal('2845000.00'),      
                        
                        '1.2.01': Decimal('1100000.00'),   
                        '1.2.02': Decimal('1800000.00'),   
                        '1.2.03': Decimal('11200000.00'),  
                        '1.2': Decimal('14100000.00'),     
                        
                        '1.3': Decimal('16945000.00'),     
                        
                        # PASIVOS
                        '2.1.01': Decimal('600000.00'),    
                        '2.1.02': Decimal('420000.00'),    
                        '2.1.03': Decimal('240000.00'),    
                        '2.1.04': Decimal('310000.00'),    
                        '2.1.05': Decimal('9800000.00'),   
                        '2.1': Decimal('11370000.00'),     
                        
                        '2.2.01': Decimal('150000.00'),    
                        '2.2.02': Decimal('1500000.00'),   
                        '2.2.03': Decimal('1850000.00'),   
                        '2.2': Decimal('3500000.00'),      
                        
                        '2.3': Decimal('14870000.00'),     
                        
                        # PATRIMONIO
                        '3.1': Decimal('1000000.00'),      
                        '3.2': Decimal('825000.00'),       
                        '3.3': Decimal('250000.00'),       
                        '3.4': Decimal('2075000.00'),      
                    },
                }
                
                for año in años:
                    # Eliminar estado existente si existe
                    EstadoFinanciero.objects.filter(
                        empresa=banco_agricola,
                        año=año,
                        tipo=TipoEstadoFinanciero.BALANCE_GENERAL
                    ).delete()
                    
                    # Crear Balance General
                    balance = EstadoFinanciero.objects.create(
                        empresa=banco_agricola,
                        año=año,
                        tipo=TipoEstadoFinanciero.BALANCE_GENERAL
                    )
                    
                    # Crear items del balance
                    datos = datos_balances[año]
                    for codigo, monto in datos.items():
                        if codigo in cuentas:
                            ItemEstadoFinanciero.objects.create(
                                estado_financiero=balance,
                                cuenta_contable=cuentas[codigo],
                                monto=monto
                            )
                    
                    self.stdout.write(
                        self.style.SUCCESS(f'  ✓ Balance General {año} creado ({balance.cantidad_cuentas} cuentas)')
                    )
                
                # Crear Estados de Resultados
                self.stdout.write(self.style.SUCCESS('\n📋 Creando Estados de Resultados...\n'))
                
                datos_resultados = {
                    2022: {
                        # INGRESOS
                        '4.1.01': Decimal('2850000.00'),   # Intereses por Préstamos
                        '4.1.02': Decimal('650000.00'),    # Comisiones por Servicios
                        '4.1': Decimal('3500000.00'),      # Ingresos Financieros
                        '4.2': Decimal('180000.00'),       # Otros Ingresos
                        '4.3': Decimal('3680000.00'),      # Total Ingresos
                        
                        # GASTOS
                        '5.1.01': Decimal('1200000.00'),   # Gastos de Personal
                        '5.1.02': Decimal('450000.00'),    # Gastos Administrativos
                        '5.1.03': Decimal('180000.00'),    # Depreciación
                        '5.1': Decimal('1830000.00'),      # Gastos Operativos
                        
                        '5.2.01': Decimal('420000.00'),    # Intereses por Obligaciones
                        '5.2': Decimal('420000.00'),       # Gastos Financieros
                        
                        '5.3.01': Decimal('280000.00'),    # Provisión para Créditos Incobrables
                        '5.3': Decimal('280000.00'),       # Provisiones
                        
                        '5.4': Decimal('2530000.00'),      # Total Gastos
                        
                        # RESULTADOS
                        '6.1': Decimal('1150000.00'),      # Utilidad Operativa
                        '6.2': Decimal('1150000.00'),      # Utilidad antes de Impuestos
                        '6.3': Decimal('345000.00'),       # Impuesto a la Renta (30%)
                        '6.4': Decimal('805000.00'),       # Utilidad Neta
                    },
                    2023: {
                        # INGRESOS
                        '4.1.01': Decimal('3250000.00'),   
                        '4.1.02': Decimal('720000.00'),    
                        '4.1': Decimal('3970000.00'),      
                        '4.2': Decimal('210000.00'),       
                        '4.3': Decimal('4180000.00'),      
                        
                        # GASTOS
                        '5.1.01': Decimal('1380000.00'),   
                        '5.1.02': Decimal('520000.00'),    
                        '5.1.03': Decimal('195000.00'),    
                        '5.1': Decimal('2095000.00'),      
                        
                        '5.2.01': Decimal('485000.00'),    
                        '5.2': Decimal('485000.00'),       
                        
                        '5.3.01': Decimal('320000.00'),    
                        '5.3': Decimal('320000.00'),       
                        
                        '5.4': Decimal('2900000.00'),      
                        
                        # RESULTADOS
                        '6.1': Decimal('1280000.00'),      
                        '6.2': Decimal('1280000.00'),      
                        '6.3': Decimal('384000.00'),       
                        '6.4': Decimal('896000.00'),       
                    },
                    2024: {
                        # INGRESOS
                        '4.1.01': Decimal('3680000.00'),   
                        '4.1.02': Decimal('820000.00'),    
                        '4.1': Decimal('4500000.00'),      
                        '4.2': Decimal('250000.00'),       
                        '4.3': Decimal('4750000.00'),      
                        
                        # GASTOS
                        '5.1.01': Decimal('1580000.00'),   
                        '5.1.02': Decimal('590000.00'),    
                        '5.1.03': Decimal('210000.00'),    
                        '5.1': Decimal('2380000.00'),      
                        
                        '5.2.01': Decimal('550000.00'),    
                        '5.2': Decimal('550000.00'),       
                        
                        '5.3.01': Decimal('360000.00'),    
                        '5.3': Decimal('360000.00'),       
                        
                        '5.4': Decimal('3290000.00'),      
                        
                        # RESULTADOS
                        '6.1': Decimal('1460000.00'),      
                        '6.2': Decimal('1460000.00'),      
                        '6.3': Decimal('438000.00'),       
                        '6.4': Decimal('1022000.00'),      
                    },
                }
                
                for año in años:
                    # Eliminar estado existente si existe
                    EstadoFinanciero.objects.filter(
                        empresa=banco_agricola,
                        año=año,
                        tipo=TipoEstadoFinanciero.ESTADO_RESULTADOS
                    ).delete()
                    
                    # Crear Estado de Resultados
                    estado_resultados = EstadoFinanciero.objects.create(
                        empresa=banco_agricola,
                        año=año,
                        tipo=TipoEstadoFinanciero.ESTADO_RESULTADOS
                    )
                    
                    # Crear items del estado de resultados
                    datos = datos_resultados[año]
                    for codigo, monto in datos.items():
                        if codigo in cuentas:
                            ItemEstadoFinanciero.objects.create(
                                estado_financiero=estado_resultados,
                                cuenta_contable=cuentas[codigo],
                                monto=monto
                            )
                    
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'  ✓ Estado de Resultados {año} creado ({estado_resultados.cantidad_cuentas} cuentas)'
                        )
                    )
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f'\n✓ Estados financieros creados: 3 Balances Generales y 3 Estados de Resultados'
                    )
                )
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'\n✗ Error: {str(e)}'))
            import traceback
            self.stdout.write(self.style.ERROR(traceback.format_exc()))
            raise
