"""
Servicio para validar la existencia de estados financieros.
"""
from apps.estados.models import EstadoFinanciero, TipoEstadoFinanciero


class ValidadorEstadosFinancieros:
    """
    Servicio para validar que existan los estados financieros necesarios
    para realizar análisis financiero.
    """
    
    @staticmethod
    def validar_estados_por_años(empresa, años):
        """
        Valida que existan ambos tipos de estados financieros (Balance General
        y Estado de Resultados) para cada año especificado.
        
        Args:
            empresa: Instancia de Empresa
            años: Lista de años (integers) a validar
            
        Returns:
            dict: {
                'valido': bool,
                'mensaje': str,
                'estados_faltantes': [
                    {
                        'año': int,
                        'balance_general': bool,
                        'estado_resultados': bool
                    }
                ]
            }
        """
        estados_faltantes = []
        
        for año in años:
            # Verificar si existe Balance General
            balance_existe = EstadoFinanciero.objects.filter(
                empresa=empresa,
                año=año,
                tipo=TipoEstadoFinanciero.BALANCE_GENERAL
            ).exists()
            
            # Verificar si existe Estado de Resultados
            resultados_existe = EstadoFinanciero.objects.filter(
                empresa=empresa,
                año=año,
                tipo=TipoEstadoFinanciero.ESTADO_RESULTADOS
            ).exists()
            
            # Si falta alguno, agregar a la lista
            if not balance_existe or not resultados_existe:
                estados_faltantes.append({
                    'año': año,
                    'balance_general': balance_existe,
                    'estado_resultados': resultados_existe
                })
        
        # Construir respuesta
        if not estados_faltantes:
            return {
                'valido': True,
                'mensaje': 'Todos los estados financieros están completos.',
                'estados_faltantes': []
            }
        else:
            mensaje = ValidadorEstadosFinancieros._construir_mensaje_error(estados_faltantes)
            return {
                'valido': False,
                'mensaje': mensaje,
                'estados_faltantes': estados_faltantes
            }
    
    @staticmethod
    def _construir_mensaje_error(estados_faltantes):
        """
        Construye un mensaje descriptivo de los estados financieros faltantes.
        
        Args:
            estados_faltantes: Lista de diccionarios con información de estados faltantes
            
        Returns:
            str: Mensaje formateado con los estados faltantes
        """
        mensajes = []
        
        for estado in estados_faltantes:
            año = estado['año']
            faltantes = []
            
            if not estado['balance_general']:
                faltantes.append('Balance General')
            
            if not estado['estado_resultados']:
                faltantes.append('Estado de Resultados')
            
            if faltantes:
                estados_texto = ' y '.join(faltantes)
                mensajes.append(f"Año {año}: Falta {estados_texto}")
        
        mensaje_principal = "No se puede generar el análisis. Faltan los siguientes estados financieros:"
        mensaje_detalle = "<br>• " + "<br>• ".join(mensajes)
        
        return mensaje_principal + mensaje_detalle
