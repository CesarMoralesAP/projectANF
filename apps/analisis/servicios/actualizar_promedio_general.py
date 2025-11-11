"""
Servicio para actualizar el promedio general de los ratios financieros.
Este promedio se calcula basándose en todos los valores calculados de todas las empresas.
"""
from decimal import Decimal
from django.db.models import Avg
from apps.catalogos.models import RatioFinanciero
from apps.analisis.models import ValorRatioCalculado


class ActualizadorPromedioGeneral:
    """
    Servicio para calcular y actualizar el promedio general de los ratios financieros.
    """
    
    @staticmethod
    def actualizar_promedios_generales():
        """
        Calcula el promedio general de cada ratio financiero basándose en todos
        los valores calculados de todas las empresas y actualiza el campo
        promedio_general en la tabla RatioFinanciero.
        
        Returns:
            dict: {
                'actualizados': int,
                'ratios': [
                    {
                        'nombre': str,
                        'promedio_anterior': Decimal,
                        'promedio_nuevo': Decimal,
                        'total_valores': int
                    }
                ]
            }
        """
        ratios_financieros = RatioFinanciero.objects.all()
        resultados = []
        actualizados = 0
        
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
                    promedio_anterior = ratio.promedio_general
                    
                    # Actualizar el ratio
                    ratio.promedio_general = round(Decimal(str(promedio)), 4)
                    ratio.save(update_fields=['promedio_general'])
                    
                    actualizados += 1
                    
                    resultados.append({
                        'nombre': ratio.nombre,
                        'promedio_anterior': promedio_anterior,
                        'promedio_nuevo': ratio.promedio_general,
                        'total_valores': valores.count()
                    })
        
        return {
            'actualizados': actualizados,
            'ratios': resultados
        }
    
    @staticmethod
    def actualizar_promedio_ratio(ratio_id):
        """
        Actualiza el promedio general de un ratio específico.
        
        Args:
            ratio_id: ID del ratio financiero a actualizar
            
        Returns:
            dict: {
                'success': bool,
                'promedio_anterior': Decimal,
                'promedio_nuevo': Decimal,
                'total_valores': int
            }
        """
        try:
            ratio = RatioFinanciero.objects.get(id=ratio_id)
            
            # Obtener todos los valores calculados de este ratio
            valores = ValorRatioCalculado.objects.filter(
                ratio=ratio,
                valor_calculado__isnull=False
            )
            
            if valores.exists():
                promedio = valores.aggregate(Avg('valor_calculado'))['valor_calculado__avg']
                
                if promedio is not None:
                    promedio_anterior = ratio.promedio_general
                    
                    ratio.promedio_general = round(Decimal(str(promedio)), 4)
                    ratio.save(update_fields=['promedio_general'])
                    
                    return {
                        'success': True,
                        'promedio_anterior': promedio_anterior,
                        'promedio_nuevo': ratio.promedio_general,
                        'total_valores': valores.count()
                    }
            
            return {
                'success': False,
                'error': 'No hay valores calculados para este ratio'
            }
            
        except RatioFinanciero.DoesNotExist:
            return {
                'success': False,
                'error': 'Ratio no encontrado'
            }
