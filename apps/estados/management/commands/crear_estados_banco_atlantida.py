from django.core.management.base import BaseCommand
from django.db import transaction
from decimal import Decimal
from apps.empresas.models import Empresa
from apps.catalogos.models import CatalogoCuenta, CuentaContable
from apps.estados.models import EstadoFinanciero, ItemEstadoFinanciero, TipoEstadoFinanciero


class Command(BaseCommand):
    """
    Comando para crear estados financieros de demostración para Banco Atlántida.
    Crea 3 Balances Generales y 3 Estados de Resultados (años 2022, 2023, 2024).
    """
    help = 'Crea estados financieros de demostración para Banco Atlántida'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('\n📊 Creando estados financieros de Banco Atlántida...\n'))
        
        try:
            with transaction.atomic():
                # Obtener Banco Atlántida
                try:
                    banco_atlantida = Empresa.objects.get(nombre='Banco Atlántida')
                except Empresa.DoesNotExist:
                    self.stdout.write(
                        self.style.ERROR('✗ Error: Banco Atlántida no existe. Ejecuta primero crear_catalogo_banco_atlantida')
                    )
                    return
                
                # Obtener catálogo
                try:
                    catalogo = CatalogoCuenta.objects.get(empresa=banco_atlantida)
                except CatalogoCuenta.DoesNotExist:
                    self.stdout.write(
                        self.style.ERROR('✗ Error: Catálogo no existe. Ejecuta primero crear_catalogo_banco_atlantida')
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
                
                # Datos con montos diferentes a Banco Agrícola pero manteniendo ecuación contable
                datos_balances = {
                    2022: {
                        # ACTIVOS
                        '1.1.01': Decimal('680000.00'),    # Caja y Bancos
                        '1.1.02': Decimal('1850000.00'),   # Cuentas por cobrar comerciales
                        '1.1.03': Decimal('520000.00'),    # Otras cuentas por cobrar
                        '1.1.04': Decimal('290000.00'),    # Inventarios
                        '1.1.05': Decimal('110000.00'),    # Gastos pagados por anticipado
                        '1.1': Decimal('3450000.00'),      # Activo Corriente
                        
                        '1.2.01': Decimal('1250000.00'),   # Inversiones en Valores
                        '1.2.02': Decimal('2100000.00'),   # Activo Fijo Neto
                        '1.2.03': Decimal('12500000.00'),  # Cartera de Créditos
                        '1.2': Decimal('15850000.00'),     # Activo No Corriente
                        
                        '1.3': Decimal('19300000.00'),     # Total Activo
                        
                        # PASIVOS
                        '2.1.01': Decimal('750000.00'),    # Sobregiros y préstamos bancarios
                        '2.1.02': Decimal('480000.00'),    # Cuentas por pagar comerciales
                        '2.1.03': Decimal('270000.00'),    # Otras cuentas por pagar
                        '2.1.04': Decimal('380000.00'),    # Parte corriente deuda largo plazo
                        '2.1.05': Decimal('11200000.00'),  # Depósitos de Clientes
                        '2.1': Decimal('13080000.00'),     # Pasivo Corriente
                        
                        '2.2.01': Decimal('180000.00'),    # Provisión CTS
                        '2.2.02': Decimal('1750000.00'),   # Deuda a largo plazo
                        '2.2.03': Decimal('2200000.00'),   # Obligaciones Financieras
                        '2.2': Decimal('4130000.00'),      # Pasivo No Corriente
                        
                        '2.3': Decimal('17210000.00'),     # Total Pasivo
                        
                        # PATRIMONIO
                        '3.1': Decimal('1500000.00'),      # Capital Social
                        '3.2': Decimal('420000.00'),       # Resultados Acumulados
                        '3.3': Decimal('170000.00'),       # Reservas
                        '3.4': Decimal('2090000.00'),      # Total Patrimonio
                    },
                    2023: {
                        # ACTIVOS
                        '1.1.01': Decimal('790000.00'),    
                        '1.1.02': Decimal('2100000.00'),   
                        '1.1.03': Decimal('620000.00'),    
                        '1.1.04': Decimal('325000.00'),    
                        '1.1.05': Decimal('135000.00'),    
                        '1.1': Decimal('3970000.00'),      
                        
                        '1.2.01': Decimal('1480000.00'),   
                        '1.2.02': Decimal('2400000.00'),   
                        '1.2.03': Decimal('14800000.00'),  
                        '1.2': Decimal('18680000.00'),     
                        
                        '1.3': Decimal('22650000.00'),     
                        
                        # PASIVOS
                        '2.1.01': Decimal('850000.00'),    
                        '2.1.02': Decimal('580000.00'),    
                        '2.1.03': Decimal('320000.00'),    
                        '2.1.04': Decimal('450000.00'),    
                        '2.1.05': Decimal('13200000.00'),  
                        '2.1': Decimal('15400000.00'),     
                        
                        '2.2.01': Decimal('210000.00'),    
                        '2.2.02': Decimal('2050000.00'),   
                        '2.2.03': Decimal('2550000.00'),   
                        '2.2': Decimal('4810000.00'),      
                        
                        '2.3': Decimal('20210000.00'),     
                        
                        # PATRIMONIO
                        '3.1': Decimal('1500000.00'),      
                        '3.2': Decimal('710000.00'),       
                        '3.3': Decimal('230000.00'),       
                        '3.4': Decimal('2440000.00'),      
                    },
                    2024: {
                        # ACTIVOS
                        '1.1.01': Decimal('920000.00'),    
                        '1.1.02': Decimal('2380000.00'),   
                        '1.1.03': Decimal('720000.00'),    
                        '1.1.04': Decimal('360000.00'),    
                        '1.1.05': Decimal('160000.00'),    
                        '1.1': Decimal('4540000.00'),      
                        
                        '1.2.01': Decimal('1750000.00'),   
                        '1.2.02': Decimal('2750000.00'),   
                        '1.2.03': Decimal('17200000.00'),  
                        '1.2': Decimal('21700000.00'),     
                        
                        '1.3': Decimal('26240000.00'),     
                        
                        # PASIVOS
                        '2.1.01': Decimal('980000.00'),    
                        '2.1.02': Decimal('680000.00'),    
                        '2.1.03': Decimal('380000.00'),    
                        '2.1.04': Decimal('530000.00'),    
                        '2.1.05': Decimal('15400000.00'),  
                        '2.1': Decimal('17970000.00'),     
                        
                        '2.2.01': Decimal('240000.00'),    
                        '2.2.02': Decimal('2400000.00'),   
                        '2.2.03': Decimal('2950000.00'),   
                        '2.2': Decimal('5590000.00'),      
                        
                        '2.3': Decimal('23560000.00'),     
                        
                        # PATRIMONIO
                        '3.1': Decimal('1500000.00'),      
                        '3.2': Decimal('940000.00'),       
                        '3.3': Decimal('240000.00'),       
                        '3.4': Decimal('2680000.00'),      
                    },
                }
                
                for año in años:
                    # Eliminar estado existente si existe
                    EstadoFinanciero.objects.filter(
                        empresa=banco_atlantida,
                        año=año,
                        tipo=TipoEstadoFinanciero.BALANCE_GENERAL
                    ).delete()
                    
                    # Crear Balance General
                    balance = EstadoFinanciero.objects.create(
                        empresa=banco_atlantida,
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
                        '4.1.01': Decimal('4200000.00'),   # Intereses por Préstamos
                        '4.1.02': Decimal('950000.00'),    # Comisiones por Servicios
                        '4.1': Decimal('5150000.00'),      # Ingresos Financieros
                        '4.2': Decimal('280000.00'),       # Otros Ingresos
                        '4.3': Decimal('5430000.00'),      # Total Ingresos
                        
                        # GASTOS
                        '5.1.01': Decimal('1850000.00'),   # Gastos de Personal
                        '5.1.02': Decimal('680000.00'),    # Gastos Administrativos
                        '5.1.03': Decimal('270000.00'),    # Depreciación
                        '5.1': Decimal('2800000.00'),      # Gastos Operativos
                        
                        '5.2.01': Decimal('620000.00'),    # Intereses por Obligaciones
                        '5.2': Decimal('620000.00'),       # Gastos Financieros
                        
                        '5.3.01': Decimal('410000.00'),    # Provisión para Créditos Incobrables
                        '5.3': Decimal('410000.00'),       # Provisiones
                        
                        '5.4': Decimal('3830000.00'),      # Total Gastos
                        
                        # RESULTADOS
                        '6.1': Decimal('1600000.00'),      # Utilidad Operativa
                        '6.2': Decimal('1600000.00'),      # Utilidad antes de Impuestos
                        '6.3': Decimal('480000.00'),       # Impuesto a la Renta (30%)
                        '6.4': Decimal('1120000.00'),      # Utilidad Neta
                    },
                    2023: {
                        # INGRESOS
                        '4.1.01': Decimal('4850000.00'),   
                        '4.1.02': Decimal('1100000.00'),   
                        '4.1': Decimal('5950000.00'),      
                        '4.2': Decimal('340000.00'),       
                        '4.3': Decimal('6290000.00'),      
                        
                        # GASTOS
                        '5.1.01': Decimal('2150000.00'),   
                        '5.1.02': Decimal('780000.00'),    
                        '5.1.03': Decimal('310000.00'),    
                        '5.1': Decimal('3240000.00'),      
                        
                        '5.2.01': Decimal('720000.00'),    
                        '5.2': Decimal('720000.00'),       
                        
                        '5.3.01': Decimal('480000.00'),    
                        '5.3': Decimal('480000.00'),       
                        
                        '5.4': Decimal('4440000.00'),      
                        
                        # RESULTADOS
                        '6.1': Decimal('1850000.00'),      
                        '6.2': Decimal('1850000.00'),      
                        '6.3': Decimal('555000.00'),       
                        '6.4': Decimal('1295000.00'),      
                    },
                    2024: {
                        # INGRESOS
                        '4.1.01': Decimal('5650000.00'),   
                        '4.1.02': Decimal('1280000.00'),   
                        '4.1': Decimal('6930000.00'),      
                        '4.2': Decimal('410000.00'),       
                        '4.3': Decimal('7340000.00'),      
                        
                        # GASTOS
                        '5.1.01': Decimal('2500000.00'),   
                        '5.1.02': Decimal('910000.00'),    
                        '5.1.03': Decimal('360000.00'),    
                        '5.1': Decimal('3770000.00'),      
                        
                        '5.2.01': Decimal('840000.00'),    
                        '5.2': Decimal('840000.00'),       
                        
                        '5.3.01': Decimal('560000.00'),    
                        '5.3': Decimal('560000.00'),       
                        
                        '5.4': Decimal('5170000.00'),      
                        
                        # RESULTADOS
                        '6.1': Decimal('2170000.00'),      
                        '6.2': Decimal('2170000.00'),      
                        '6.3': Decimal('651000.00'),       
                        '6.4': Decimal('1519000.00'),      
                    },
                }
                
                for año in años:
                    # Eliminar estado existente si existe
                    EstadoFinanciero.objects.filter(
                        empresa=banco_atlantida,
                        año=año,
                        tipo=TipoEstadoFinanciero.ESTADO_RESULTADOS
                    ).delete()
                    
                    # Crear Estado de Resultados
                    estado_resultados = EstadoFinanciero.objects.create(
                        empresa=banco_atlantida,
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
