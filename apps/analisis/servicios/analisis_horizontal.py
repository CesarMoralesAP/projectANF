"""
Servicio para realizar análisis horizontal de estados financieros.
Calcula las variaciones absolutas y porcentuales año tras año.
"""
from decimal import Decimal, InvalidOperation
from apps.estados.models import EstadoFinanciero, ItemEstadoFinanciero, TipoEstadoFinanciero
from apps.catalogos.models import TipoCuenta


class AnalizadorHorizontal:
    """
    Clase para realizar análisis horizontal de estados financieros.
    Calcula variaciones absolutas y porcentuales entre años consecutivos.
    """
    
    @staticmethod
    def analizar_balance_general(empresa, años):
        """
        Realiza el análisis horizontal del Balance General.
        
        Args:
            empresa: Instancia de Empresa
            años: Lista de años ordenados (de menor a mayor)
        
        Returns:
            dict: Datos estructurados para el análisis horizontal
        """
        # Validar que haya al menos 2 años
        if len(años) < 2:
            return {
                'error': 'Se necesitan al menos 2 años para realizar el análisis horizontal.'
            }
        
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
        
        # Obtener todas las cuentas únicas del catálogo de la empresa
        # Solo las que aparecen en algún estado financiero
        cuentas_ids = set()
        for estado in estados:
            cuentas_ids.update(estado.items.values_list('cuenta_contable_id', flat=True))
        
        # Obtener información de las cuentas
        from apps.catalogos.models import CuentaContable
        cuentas = CuentaContable.objects.filter(
            id__in=cuentas_ids,
            tipo__in=[TipoCuenta.ACTIVO, TipoCuenta.PASIVO, TipoCuenta.PATRIMONIO]
        ).select_related('catalogo').order_by('tipo', 'codigo')
        
        # Construir estructura de datos con montos por año
        datos_cuentas = {}
        for cuenta in cuentas:
            datos_cuentas[cuenta.id] = {
                'id': cuenta.id,
                'codigo': cuenta.codigo,
                'nombre': cuenta.nombre,
                'tipo': cuenta.tipo,
                'tipo_display': cuenta.get_tipo_display(),
                'montos_por_año': {}
            }
        
        # Llenar montos por año para cada cuenta
        for estado in estados:
            año = estado.año
            for item in estado.items.all():
                cuenta_id = item.cuenta_contable_id
                if cuenta_id in datos_cuentas:
                    datos_cuentas[cuenta_id]['montos_por_año'][año] = item.monto
        
        # Calcular variaciones entre años consecutivos
        años_ordenados = sorted(años)
        variaciones_info = []
        
        for i in range(len(años_ordenados) - 1):
            año_base = años_ordenados[i]
            año_siguiente = años_ordenados[i + 1]
            variaciones_info.append({
                'año_base': año_base,
                'año_siguiente': año_siguiente,
                'label': f'{año_base}-{año_siguiente}'
            })
        
        # Calcular variaciones para cada cuenta
        for cuenta_id, datos in datos_cuentas.items():
            datos['variaciones'] = {}
            
            for var_info in variaciones_info:
                año_base = var_info['año_base']
                año_siguiente = var_info['año_siguiente']
                label = var_info['label']
                
                monto_base = datos['montos_por_año'].get(año_base)
                monto_siguiente = datos['montos_por_año'].get(año_siguiente)
                
                if monto_base is not None and monto_siguiente is not None:
                    # Calcular variación absoluta
                    variacion_absoluta = monto_siguiente - monto_base
                    
                    # Calcular variación porcentual
                    if monto_base != 0:
                        variacion_porcentual = (variacion_absoluta / abs(monto_base)) * 100
                    else:
                        # Si el monto base es 0, la variación porcentual es N/A
                        variacion_porcentual = None
                    
                    datos['variaciones'][label] = {
                        'variacion_absoluta': variacion_absoluta,
                        'variacion_porcentual': variacion_porcentual
                    }
                else:
                    datos['variaciones'][label] = {
                        'variacion_absoluta': None,
                        'variacion_porcentual': None
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
        
        return {
            'success': True,
            'empresa': {
                'id': empresa.id,
                'nombre': empresa.nombre,
                'sector': empresa.sector.nombre
            },
            'años': años_ordenados,
            'variaciones_info': variaciones_info,
            'cuentas_por_tipo': {
                'ACTIVO': cuentas_por_tipo[TipoCuenta.ACTIVO],
                'PASIVO': cuentas_por_tipo[TipoCuenta.PASIVO],
                'PATRIMONIO': cuentas_por_tipo[TipoCuenta.PATRIMONIO]
            }
        }
    
    @staticmethod
    def analizar_estado_resultados(empresa, años):
        """
        Realiza el análisis horizontal del Estado de Resultados.
        
        Args:
            empresa: Instancia de Empresa
            años: Lista de años ordenados (de menor a mayor)
        
        Returns:
            dict: Datos estructurados para el análisis horizontal
        """
        # Validar que haya al menos 2 años
        if len(años) < 2:
            return {
                'error': 'Se necesitan al menos 2 años para realizar el análisis horizontal.'
            }
        
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
        
        # Obtener todas las cuentas únicas del catálogo de la empresa
        cuentas_ids = set()
        for estado in estados:
            cuentas_ids.update(estado.items.values_list('cuenta_contable_id', flat=True))
        
        # Obtener información de las cuentas
        from apps.catalogos.models import CuentaContable
        cuentas = CuentaContable.objects.filter(
            id__in=cuentas_ids,
            tipo__in=[TipoCuenta.INGRESO, TipoCuenta.GASTO, TipoCuenta.RESULTADO]
        ).select_related('catalogo').order_by('tipo', 'codigo')
        
        # Construir estructura de datos con montos por año
        datos_cuentas = {}
        for cuenta in cuentas:
            datos_cuentas[cuenta.id] = {
                'id': cuenta.id,
                'codigo': cuenta.codigo,
                'nombre': cuenta.nombre,
                'tipo': cuenta.tipo,
                'tipo_display': cuenta.get_tipo_display(),
                'montos_por_año': {}
            }
        
        # Llenar montos por año para cada cuenta
        for estado in estados:
            año = estado.año
            for item in estado.items.all():
                cuenta_id = item.cuenta_contable_id
                if cuenta_id in datos_cuentas:
                    datos_cuentas[cuenta_id]['montos_por_año'][año] = item.monto
        
        # Calcular variaciones entre años consecutivos
        años_ordenados = sorted(años)
        variaciones_info = []
        
        for i in range(len(años_ordenados) - 1):
            año_base = años_ordenados[i]
            año_siguiente = años_ordenados[i + 1]
            variaciones_info.append({
                'año_base': año_base,
                'año_siguiente': año_siguiente,
                'label': f'{año_base}-{año_siguiente}'
            })
        
        # Calcular variaciones para cada cuenta
        for cuenta_id, datos in datos_cuentas.items():
            datos['variaciones'] = {}
            
            for var_info in variaciones_info:
                año_base = var_info['año_base']
                año_siguiente = var_info['año_siguiente']
                label = var_info['label']
                
                monto_base = datos['montos_por_año'].get(año_base)
                monto_siguiente = datos['montos_por_año'].get(año_siguiente)
                
                if monto_base is not None and monto_siguiente is not None:
                    # Calcular variación absoluta
                    variacion_absoluta = monto_siguiente - monto_base
                    
                    # Calcular variación porcentual
                    if monto_base != 0:
                        variacion_porcentual = (variacion_absoluta / abs(monto_base)) * 100
                    else:
                        variacion_porcentual = None
                    
                    datos['variaciones'][label] = {
                        'variacion_absoluta': variacion_absoluta,
                        'variacion_porcentual': variacion_porcentual
                    }
                else:
                    datos['variaciones'][label] = {
                        'variacion_absoluta': None,
                        'variacion_porcentual': None
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
        
        return {
            'success': True,
            'empresa': {
                'id': empresa.id,
                'nombre': empresa.nombre,
                'sector': empresa.sector.nombre
            },
            'años': años_ordenados,
            'variaciones_info': variaciones_info,
            'cuentas_por_tipo': {
                'INGRESO': cuentas_por_tipo[TipoCuenta.INGRESO],
                'GASTO': cuentas_por_tipo[TipoCuenta.GASTO],
                'RESULTADO': cuentas_por_tipo[TipoCuenta.RESULTADO]
            }
        }
