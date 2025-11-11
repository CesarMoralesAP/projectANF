"""
Servicio para calcular ratios financieros basados en estados financieros.
"""
from decimal import Decimal, InvalidOperation
from django.db import transaction
from django.db.models import Avg
from apps.catalogos.models import RatioFinanciero, MapeoCuentaRatio
from apps.estados.models import EstadoFinanciero, ItemEstadoFinanciero, TipoEstadoFinanciero
from apps.parametros.models import RatioReferenciaSector
from apps.analisis.models import ValorRatioCalculado


class CalculadoraRatios:
    """
    Servicio para calcular ratios financieros a partir de estados financieros.
    """
    
    @staticmethod
    def calcular_ratios_por_años(empresa, años, usuario=None):
        """
        Calcula todos los ratios financieros para una empresa en los años especificados
        y guarda los resultados en la base de datos.
        
        Args:
            empresa: Instancia de Empresa
            años: Lista de años (integers)
            usuario: Usuario que genera el cálculo (opcional)
            
        Returns:
            dict: {
                'ratios': [
                    {
                        'nombre': str,
                        'categoria': str,
                        'parametro_sectorial': Decimal,
                        'promedio_sector': Decimal,
                        'promedio_general': Decimal,
                        'valores_por_año': {
                            año: {
                                'valor': Decimal,
                                'superior_parametro': bool,
                                'superior_promedio_sector': bool,
                                'superior_promedio_general': bool
                            }
                        }
                    }
                ]
            }
        """
        # Obtener el catálogo de la empresa
        try:
            catalogo = empresa.catalogo_cuenta
        except:
            return {'ratios': [], 'error': 'Empresa sin catálogo configurado'}
        
        # Obtener todos los ratios financieros
        ratios_financieros = RatioFinanciero.objects.prefetch_related(
            'componentes'
        ).order_by('categoria', 'nombre')
        
        resultados = []
        
        with transaction.atomic():
            # Eliminar cálculos anteriores para estos años (recalcular)
            ValorRatioCalculado.objects.filter(
                empresa=empresa,
                año__in=años
            ).delete()
            
            for ratio in ratios_financieros:
                # Obtener parámetro sectorial para esta empresa
                try:
                    referencia_sector = RatioReferenciaSector.objects.get(
                        ratio_financiero=ratio,
                        sector=empresa.sector
                    )
                    parametro_sectorial = referencia_sector.valor_optimo
                    promedio_sector = referencia_sector.promedio_sector
                except RatioReferenciaSector.DoesNotExist:
                    parametro_sectorial = None
                    promedio_sector = None
                
                # Promedio general
                promedio_general = ratio.promedio_general
                
                # Calcular valores para cada año
                valores_por_año = {}
                
                for año in años:
                    valor_ratio = CalculadoraRatios._calcular_ratio_año(
                        ratio, catalogo, empresa, año
                    )
                    
                    if valor_ratio is not None:
                        # Comparaciones
                        superior_parametro = (
                            parametro_sectorial is not None and 
                            valor_ratio >= parametro_sectorial
                        )
                        superior_promedio_sector = (
                            promedio_sector is not None and 
                            valor_ratio >= promedio_sector
                        )
                        superior_promedio_general = (
                            promedio_general is not None and 
                            valor_ratio >= promedio_general
                        )
                        
                        # Guardar en base de datos
                        ValorRatioCalculado.objects.create(
                            empresa=empresa,
                            ratio=ratio,
                            año=año,
                            valor_calculado=valor_ratio,
                            parametro_sectorial=parametro_sectorial,
                            promedio_sector=promedio_sector,
                            promedio_general=promedio_general,
                            superior_parametro_sectorial=superior_parametro,
                            superior_promedio_sector=superior_promedio_sector,
                            superior_promedio_general=superior_promedio_general,
                            usuario_calculo=usuario
                        )
                        
                        valores_por_año[año] = {
                            'valor': valor_ratio,
                            'superior_parametro': superior_parametro,
                            'superior_promedio_sector': superior_promedio_sector,
                            'superior_promedio_general': superior_promedio_general
                        }
                    else:
                        valores_por_año[año] = None
                
                # Solo agregar el ratio si tiene al menos un valor calculado
                if any(v is not None for v in valores_por_año.values()):
                    resultados.append({
                        'nombre': ratio.nombre,
                        'categoria': ratio.categoria,
                        'formula': ratio.formula_display,
                        'parametro_sectorial': parametro_sectorial,
                        'promedio_sector': promedio_sector,
                        'promedio_general': promedio_general,
                        'valores_por_año': valores_por_año
                    })
            
            # Actualizar promedios generales de todos los ratios con nuevos valores
            CalculadoraRatios._actualizar_promedios_generales(ratios_financieros)
        
        return {'ratios': resultados}
    
    @staticmethod
    def _calcular_ratio_año(ratio, catalogo, empresa, año):
        """
        Calcula el valor de un ratio específico para un año.
        
        Args:
            ratio: Instancia de RatioFinanciero
            catalogo: Instancia de CatalogoCuenta
            empresa: Instancia de Empresa
            año: Año a calcular
            
        Returns:
            Decimal o None si no se puede calcular
        """
        # Obtener los componentes del ratio
        componentes = ratio.componentes.all()
        
        if not componentes:
            return None
        
        # Obtener mapeos de componentes a cuentas
        valores_componentes = []
        
        for componente in componentes:
            # Buscar el mapeo de este componente en el catálogo de la empresa
            try:
                mapeo = MapeoCuentaRatio.objects.get(
                    catalogo_cuenta=catalogo,
                    componente_ratio=componente
                )
                
                if not mapeo.cuenta_contable:
                    return None  # No hay cuenta mapeada
                
                # Obtener el valor de esta cuenta en los estados financieros del año
                valor = CalculadoraRatios._obtener_valor_cuenta(
                    mapeo.cuenta_contable, empresa, año
                )
                
                if valor is None:
                    return None
                
                valores_componentes.append(valor)
                
            except MapeoCuentaRatio.DoesNotExist:
                return None  # No hay mapeo configurado
        
        # Calcular el ratio según la cantidad de componentes y el nombre del ratio
        if len(valores_componentes) == 2:
            # Ratios simples: Numerador / Denominador
            numerador = valores_componentes[0]
            denominador = valores_componentes[1]
            
            if denominador == 0:
                return None
            
            try:
                resultado = numerador / denominador
                return round(resultado, 4)
            except (InvalidOperation, ZeroDivisionError):
                return None
        
        elif len(valores_componentes) == 3 and ratio.nombre == "Prueba Ácida":
            # Prueba Ácida: (Activo Corriente - Inventario) / Pasivo Corriente
            # Componentes: [Activo Corriente, Inventario, Pasivo Corriente]
            activo_corriente = valores_componentes[0]
            inventario = valores_componentes[1]
            pasivo_corriente = valores_componentes[2]
            
            if pasivo_corriente == 0:
                return None
            
            try:
                numerador = activo_corriente - inventario
                resultado = numerador / pasivo_corriente
                return round(resultado, 4)
            except (InvalidOperation, ZeroDivisionError):
                return None
        
        # Para otros casos, retornar None
        return None
    
    @staticmethod
    def _obtener_valor_cuenta(cuenta_contable, empresa, año):
        """
        Obtiene el valor de una cuenta contable en los estados financieros de un año.
        
        Args:
            cuenta_contable: Instancia de CuentaContable
            empresa: Instancia de Empresa
            año: Año del estado financiero
            
        Returns:
            Decimal o None si no se encuentra
        """
        # Buscar en ambos tipos de estados financieros
        from apps.estados.models import TipoEstadoFinanciero
        
        # Primero intentar en Balance General
        try:
            estado = EstadoFinanciero.objects.get(
                empresa=empresa,
                año=año,
                tipo=TipoEstadoFinanciero.BALANCE_GENERAL
            )
            
            item = ItemEstadoFinanciero.objects.get(
                estado_financiero=estado,
                cuenta_contable=cuenta_contable
            )
            
            return item.monto
        except (EstadoFinanciero.DoesNotExist, ItemEstadoFinanciero.DoesNotExist):
            pass
        
        # Luego intentar en Estado de Resultados
        try:
            estado = EstadoFinanciero.objects.get(
                empresa=empresa,
                año=año,
                tipo=TipoEstadoFinanciero.ESTADO_RESULTADOS
            )
            
            item = ItemEstadoFinanciero.objects.get(
                estado_financiero=estado,
                cuenta_contable=cuenta_contable
            )
            
            return item.monto
        except (EstadoFinanciero.DoesNotExist, ItemEstadoFinanciero.DoesNotExist):
            pass
        
        return None
    
    @staticmethod
    def _actualizar_promedios_generales(ratios_financieros):
        """
        Actualiza el promedio general de cada ratio financiero basándose en todos
        los valores calculados de todas las empresas.
        
        Args:
            ratios_financieros: QuerySet de RatioFinanciero
        """
        for ratio in ratios_financieros:
            # Obtener todos los valores calculados de este ratio (todas las empresas, todos los años)
            valores = ValorRatioCalculado.objects.filter(
                ratio=ratio,
                valor_calculado__isnull=False
            )
            
            if valores.exists():
                # Calcular promedio
                promedio = valores.aggregate(Avg('valor_calculado'))['valor_calculado__avg']
                
                if promedio is not None:
                    # Actualizar el ratio
                    ratio.promedio_general = round(Decimal(str(promedio)), 4)
                    ratio.save(update_fields=['promedio_general', 'actualizado_en'])
