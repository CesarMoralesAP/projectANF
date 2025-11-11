"""
Servicio para realizar análisis vertical de estados financieros.
Calcula el porcentaje de cada cuenta sobre una base:
- Balance General: % sobre Activo Total
- Estado de Resultados: % sobre Ingresos/Ventas Totales
"""
from decimal import Decimal, InvalidOperation
from apps.estados.models import EstadoFinanciero, ItemEstadoFinanciero, TipoEstadoFinanciero
from apps.catalogos.models import TipoCuenta


class AnalizadorVertical:
    """
    Clase para realizar análisis vertical de estados financieros.
    Calcula porcentajes de participación sobre una base común.
    """
    
    @staticmethod
    def analizar_balance_general(empresa, años):
        """
        Realiza el análisis vertical del Balance General.
        Calcula % sobre su propio total para cada tipo:
        - Activos: cuenta/activo total * 100
        - Pasivos: cuenta/pasivo total * 100
        - Patrimonio: cuenta/patrimonio total * 100
        
        Args:
            empresa: Instancia de Empresa
            años: Lista de años ordenados (de menor a mayor)
        
        Returns:
            dict: Datos estructurados para el análisis vertical
        """
        # Obtener los estados financieros de Balance General
        estados = EstadoFinanciero.objects.filter(
            empresa=empresa,
            año__in=años,
            tipo=TipoEstadoFinanciero.BALANCE_GENERAL
        ).prefetch_related('items__cuenta_contable').order_by('año')
        
        if not estados.exists():
            return {
                'error': 'No se encontraron estados financieros de Balance General para los años seleccionados.'
            }
        
        # Palabras clave para identificar cuentas de totales
        palabras_total = ['total', 'suma', 'total general', 'total activo', 'total pasivo', 
                         'total patrimonio', 'total de', 'totales']
        
        # Calcular totales por tipo y por año (excluyendo cuentas de totales)
        totales_por_tipo_año = {
            TipoCuenta.ACTIVO: {},
            TipoCuenta.PASIVO: {},
            TipoCuenta.PATRIMONIO: {}
        }
        
        for estado in estados:
            año = estado.año
            
            # Calcular Activo Total (excluyendo cuentas que ya son totales)
            activo_total = Decimal('0')
            for item in estado.items.filter(cuenta_contable__tipo=TipoCuenta.ACTIVO):
                cuenta_nombre = item.cuenta_contable.nombre.lower()
                es_cuenta_total = any(palabra in cuenta_nombre for palabra in palabras_total)
                if not es_cuenta_total:
                    activo_total += item.monto
            totales_por_tipo_año[TipoCuenta.ACTIVO][año] = activo_total
            
            # Calcular Pasivo Total (excluyendo cuentas que ya son totales)
            pasivo_total = Decimal('0')
            for item in estado.items.filter(cuenta_contable__tipo=TipoCuenta.PASIVO):
                cuenta_nombre = item.cuenta_contable.nombre.lower()
                es_cuenta_total = any(palabra in cuenta_nombre for palabra in palabras_total)
                if not es_cuenta_total:
                    pasivo_total += item.monto
            totales_por_tipo_año[TipoCuenta.PASIVO][año] = pasivo_total
            
            # Calcular Patrimonio Total (excluyendo cuentas que ya son totales)
            patrimonio_total = Decimal('0')
            for item in estado.items.filter(cuenta_contable__tipo=TipoCuenta.PATRIMONIO):
                cuenta_nombre = item.cuenta_contable.nombre.lower()
                es_cuenta_total = any(palabra in cuenta_nombre for palabra in palabras_total)
                if not es_cuenta_total:
                    patrimonio_total += item.monto
            totales_por_tipo_año[TipoCuenta.PATRIMONIO][año] = patrimonio_total
        
        # Obtener todas las cuentas únicas del catálogo de la empresa
        cuentas_ids = set()
        for estado in estados:
            cuentas_ids.update(estado.items.values_list('cuenta_contable_id', flat=True))
        
        # Obtener información de las cuentas
        from apps.catalogos.models import CuentaContable
        cuentas = CuentaContable.objects.filter(
            id__in=cuentas_ids,
            tipo__in=[TipoCuenta.ACTIVO, TipoCuenta.PASIVO, TipoCuenta.PATRIMONIO]
        ).select_related('catalogo').order_by('tipo', 'codigo')
        
        # Construir estructura de datos con montos y porcentajes por año
        datos_cuentas = {}
        for cuenta in cuentas:
            datos_cuentas[cuenta.id] = {
                'id': cuenta.id,
                'codigo': cuenta.codigo,
                'nombre': cuenta.nombre,
                'tipo': cuenta.tipo,
                'tipo_display': cuenta.get_tipo_display(),
                'datos_por_año': {}
            }
        
        # Llenar montos y calcular porcentajes por año para cada cuenta
        for estado in estados:
            año = estado.año
            
            for item in estado.items.all():
                cuenta_id = item.cuenta_contable_id
                if cuenta_id in datos_cuentas:
                    cuenta_tipo = datos_cuentas[cuenta_id]['tipo']
                    cuenta_nombre = datos_cuentas[cuenta_id]['nombre'].lower()
                    monto = item.monto
                    
                    # Identificar si es una cuenta de total/suma (usar la misma lista definida arriba)
                    es_cuenta_total = any(palabra in cuenta_nombre for palabra in palabras_total)
                    
                    # Obtener el total correspondiente según el tipo de cuenta
                    total_tipo = totales_por_tipo_año[cuenta_tipo].get(año, Decimal('0'))
                    
                    # Si es una cuenta de total, asignar 100%, si no, calcular el porcentaje
                    if es_cuenta_total:
                        porcentaje = Decimal('100')
                    elif total_tipo != 0:
                        porcentaje = (monto / total_tipo) * 100
                    else:
                        porcentaje = Decimal('0')
                    
                    datos_cuentas[cuenta_id]['datos_por_año'][año] = {
                        'monto': monto,
                        'porcentaje': porcentaje
                    }
        
        # Organizar cuentas por tipo
        cuentas_por_tipo = {
            TipoCuenta.ACTIVO: [],
            TipoCuenta.PASIVO: [],
            TipoCuenta.PATRIMONIO: []
        }
        
        for cuenta_data in datos_cuentas.values():
            tipo = cuenta_data['tipo']
            if tipo in cuentas_por_tipo:
                cuentas_por_tipo[tipo].append(cuenta_data)
        
        # Ordenar años
        años_ordenados = sorted(años)
        
        return {
            'success': True,
            'empresa': {
                'id': empresa.id,
                'nombre': empresa.nombre,
                'sector': empresa.sector.nombre
            },
            'años': años_ordenados,
            'base_calculo': 'Por Tipo',
            'totales_por_tipo_año': {
                'ACTIVO': {año: float(total) for año, total in totales_por_tipo_año[TipoCuenta.ACTIVO].items()},
                'PASIVO': {año: float(total) for año, total in totales_por_tipo_año[TipoCuenta.PASIVO].items()},
                'PATRIMONIO': {año: float(total) for año, total in totales_por_tipo_año[TipoCuenta.PATRIMONIO].items()}
            },
            'cuentas_por_tipo': {
                'ACTIVO': cuentas_por_tipo[TipoCuenta.ACTIVO],
                'PASIVO': cuentas_por_tipo[TipoCuenta.PASIVO],
                'PATRIMONIO': cuentas_por_tipo[TipoCuenta.PATRIMONIO]
            }
        }
    
    @staticmethod
    def analizar_estado_resultados(empresa, años):
        """
        Realiza el análisis vertical del Estado de Resultados.
        Calcula % sobre Ingresos/Ventas Totales para cada cuenta.
        
        Args:
            empresa: Instancia de Empresa
            años: Lista de años ordenados (de menor a mayor)
        
        Returns:
            dict: Datos estructurados para el análisis vertical
        """
        # Obtener los estados financieros de Estado de Resultados
        estados = EstadoFinanciero.objects.filter(
            empresa=empresa,
            año__in=años,
            tipo=TipoEstadoFinanciero.ESTADO_RESULTADOS
        ).prefetch_related('items__cuenta_contable').order_by('año')
        
        if not estados.exists():
            return {
                'error': 'No se encontraron estados financieros de Estado de Resultados para los años seleccionados.'
            }
        
        # Identificar cuenta de Ingresos/Ventas Totales
        # Buscar cuentas de tipo INGRESO que contengan "ventas" o "ingresos" en el nombre
        from apps.catalogos.models import CuentaContable
        
        # Obtener todas las cuentas de ingreso del catálogo de la empresa
        cuentas_ingreso = CuentaContable.objects.filter(
            catalogo__empresa=empresa,
            tipo=TipoCuenta.INGRESO
        ).order_by('codigo')
        
        # Intentar encontrar la cuenta principal de ingresos/ventas
        # Prioridad: buscar por palabras clave en el nombre
        cuenta_base = None
        palabras_clave = ['ventas totales', 'ingresos totales', 'ventas', 'ingresos operacionales', 'ventas netas']
        
        for palabra in palabras_clave:
            cuenta_encontrada = cuentas_ingreso.filter(nombre__icontains=palabra).first()
            if cuenta_encontrada:
                cuenta_base = cuenta_encontrada
                break
        
        # Si no se encuentra, usar la primera cuenta de ingresos (generalmente es la principal)
        if not cuenta_base and cuentas_ingreso.exists():
            cuenta_base = cuentas_ingreso.first()
        
        if not cuenta_base:
            return {
                'error': 'No se encontró una cuenta de Ingresos/Ventas en el catálogo de la empresa. '
                         'Verifique que exista al menos una cuenta de tipo INGRESO.'
            }
        
        # Palabras clave para identificar cuentas de totales (reutilizar del Balance General)
        palabras_total = ['total', 'suma', 'total general', 'total activo', 'total pasivo', 
                         'total patrimonio', 'total de', 'totales', 'total ingresos', 
                         'total ventas', 'total gastos', 'utilidad', 'resultado']
        
        # Calcular Ingresos Totales por año (excluyendo cuentas de totales)
        ingresos_totales_por_año = {}
        cuenta_base_usada = {
            'codigo': cuenta_base.codigo,
            'nombre': cuenta_base.nombre
        }
        
        for estado in estados:
            # Sumar todos los ingresos EXCEPTO las cuentas de totales
            ingresos_total = Decimal('0')
            for item in estado.items.filter(cuenta_contable__tipo=TipoCuenta.INGRESO):
                cuenta_nombre = item.cuenta_contable.nombre.lower()
                es_cuenta_total = any(palabra in cuenta_nombre for palabra in palabras_total)
                if not es_cuenta_total:
                    ingresos_total += item.monto
            ingresos_totales_por_año[estado.año] = ingresos_total
        
        # Obtener todas las cuentas únicas del catálogo de la empresa
        cuentas_ids = set()
        for estado in estados:
            cuentas_ids.update(estado.items.values_list('cuenta_contable_id', flat=True))
        
        # Obtener información de las cuentas
        cuentas = CuentaContable.objects.filter(
            id__in=cuentas_ids,
            tipo__in=[TipoCuenta.INGRESO, TipoCuenta.GASTO, TipoCuenta.RESULTADO]
        ).select_related('catalogo').order_by('tipo', 'codigo')
        
        # Construir estructura de datos con montos y porcentajes por año
        datos_cuentas = {}
        for cuenta in cuentas:
            datos_cuentas[cuenta.id] = {
                'id': cuenta.id,
                'codigo': cuenta.codigo,
                'nombre': cuenta.nombre,
                'tipo': cuenta.tipo,
                'tipo_display': cuenta.get_tipo_display(),
                'datos_por_año': {}
            }
        
        # Llenar montos y calcular porcentajes por año para cada cuenta
        for estado in estados:
            año = estado.año
            ingresos_totales = ingresos_totales_por_año[año]
            
            for item in estado.items.all():
                cuenta_id = item.cuenta_contable_id
                if cuenta_id in datos_cuentas:
                    cuenta_nombre = datos_cuentas[cuenta_id]['nombre'].lower()
                    monto = item.monto
                    
                    # Identificar si es una cuenta de total/suma
                    es_cuenta_total = any(palabra in cuenta_nombre for palabra in palabras_total)
                    
                    # Si es una cuenta de total, asignar 100%, si no, calcular el porcentaje
                    if es_cuenta_total:
                        porcentaje = Decimal('100')
                    elif ingresos_totales != 0:
                        porcentaje = (monto / ingresos_totales) * 100
                    else:
                        porcentaje = Decimal('0')
                    
                    datos_cuentas[cuenta_id]['datos_por_año'][año] = {
                        'monto': monto,
                        'porcentaje': porcentaje
                    }
        
        # Organizar cuentas por tipo
        cuentas_por_tipo = {
            TipoCuenta.INGRESO: [],
            TipoCuenta.GASTO: [],
            TipoCuenta.RESULTADO: []
        }
        
        for cuenta_data in datos_cuentas.values():
            tipo = cuenta_data['tipo']
            if tipo in cuentas_por_tipo:
                cuentas_por_tipo[tipo].append(cuenta_data)
        
        # Ordenar años
        años_ordenados = sorted(años)
        
        return {
            'success': True,
            'empresa': {
                'id': empresa.id,
                'nombre': empresa.nombre,
                'sector': empresa.sector.nombre
            },
            'años': años_ordenados,
            'base_calculo': cuenta_base_usada['nombre'],
            'cuenta_base_usada': cuenta_base_usada,
            'ingresos_totales_por_año': {año: float(total) for año, total in ingresos_totales_por_año.items()},
            'cuentas_por_tipo': {
                'INGRESO': cuentas_por_tipo[TipoCuenta.INGRESO],
                'GASTO': cuentas_por_tipo[TipoCuenta.GASTO],
                'RESULTADO': cuentas_por_tipo[TipoCuenta.RESULTADO]
            }
        }
