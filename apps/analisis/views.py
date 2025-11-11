from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.views import View
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from decimal import Decimal
from apps.empresas.models import Empresa
from apps.analisis.servicios.validar_estados import ValidadorEstadosFinancieros
from apps.analisis.servicios.calcular_ratios import CalculadoraRatios
from apps.analisis.servicios.analisis_horizontal import AnalizadorHorizontal
from apps.analisis.servicios.analisis_vertical import AnalizadorVertical


def convertir_decimales(obj):
    """
    Convierte objetos Decimal a float para serialización JSON.
    """
    if isinstance(obj, Decimal):
        return float(obj)
    elif isinstance(obj, dict):
        return {key: convertir_decimales(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convertir_decimales(item) for item in obj]
    return obj


class AnalisisFinancieroView(LoginRequiredMixin, TemplateView):
    """
    Vista principal para el módulo de informes y análisis financiero.
    Permite seleccionar empresa y años para generar análisis.
    """
    template_name = 'analisis/analisis_financiero.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Obtener todas las empresas ordenadas por nombre
        context['empresas'] = Empresa.objects.select_related('sector').order_by('nombre')
        
        # Obtener años disponibles desde la base de datos de estados financieros
        from apps.estados.models import EstadoFinanciero
        años_disponibles = EstadoFinanciero.objects.values_list('año', flat=True).distinct().order_by('-año')
        context['años_disponibles'] = list(años_disponibles)
        
        return context


@method_decorator(require_http_methods(["POST"]), name='dispatch')
class ValidarEstadosView(LoginRequiredMixin, View):
    """
    Vista para validar que existan los estados financieros necesarios
    antes de generar el análisis.
    """
    
    def post(self, request):
        try:
            # Obtener datos del POST
            empresa_id = request.POST.get('empresa_id')
            años_seleccionados = request.POST.getlist('años[]')
            
            # Validar que se hayan enviado datos
            if not empresa_id:
                return JsonResponse({
                    'success': False,
                    'mensaje': 'Debe seleccionar una empresa.'
                })
            
            if not años_seleccionados:
                return JsonResponse({
                    'success': False,
                    'mensaje': 'Debe seleccionar al menos un año.'
                })
            
            # Obtener la empresa
            try:
                empresa = Empresa.objects.get(id=empresa_id)
            except Empresa.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'mensaje': 'La empresa seleccionada no existe.'
                })
            
            # Convertir años a enteros
            años = [int(año) for año in años_seleccionados]
            años.sort()  # Ordenar para mostrar en orden cronológico
            
            # Validar estados financieros
            resultado = ValidadorEstadosFinancieros.validar_estados_por_años(empresa, años)
            
            if resultado['valido']:
                # Calcular ratios financieros y GUARDAR en BD
                ratios_data = CalculadoraRatios.calcular_ratios_por_años(
                    empresa, 
                    años,
                    usuario=request.user  # Pasar el usuario actual
                )
                
                if ratios_data.get('error'):
                    return JsonResponse({
                        'success': False,
                        'mensaje': ratios_data['error']
                    })
                
                # Convertir Decimales a float para JSON
                ratios_convertidos = convertir_decimales(ratios_data['ratios'])
                
                return JsonResponse({
                    'success': True,
                    'mensaje': f'¡Análisis generado y guardado exitosamente para {empresa.nombre}!<br>Años analizados: {", ".join(map(str, años))}',
                    'ratios': ratios_convertidos,
                    'años': años,
                    'empresa': {
                        'id': empresa.id,
                        'nombre': empresa.nombre,
                        'sector': empresa.sector.nombre
                    }
                })
            else:
                return JsonResponse({
                    'success': False,
                    'mensaje': resultado['mensaje'],
                    'estados_faltantes': resultado['estados_faltantes']
                })
                
        except Exception as e:
                return JsonResponse({
                    'success': False,
                    'mensaje': f'Error al procesar la solicitud: {str(e)}'
                })


@method_decorator(require_http_methods(["POST"]), name='dispatch')
class AnalisisHorizontalBalanceView(LoginRequiredMixin, View):
    """
    Vista para generar análisis horizontal del Balance General.
    """
    
    def post(self, request):
        try:
            # Obtener datos del POST
            empresa_id = request.POST.get('empresa_id')
            años_seleccionados = request.POST.getlist('años[]')
            
            # Validar datos
            if not empresa_id:
                return JsonResponse({
                    'success': False,
                    'mensaje': 'Debe seleccionar una empresa.'
                })
            
            if not años_seleccionados or len(años_seleccionados) < 2:
                return JsonResponse({
                    'success': False,
                    'mensaje': 'Se necesitan al menos 2 años para realizar el análisis horizontal.'
                })
            
            # Obtener empresa
            try:
                empresa = Empresa.objects.get(id=empresa_id)
            except Empresa.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'mensaje': 'La empresa seleccionada no existe.'
                })
            
            # Convertir años a enteros y ordenar
            años = sorted([int(año) for año in años_seleccionados])
            
            # Realizar análisis horizontal
            resultado = AnalizadorHorizontal.analizar_balance_general(empresa, años)
            
            if resultado.get('error'):
                return JsonResponse({
                    'success': False,
                    'mensaje': resultado['error']
                })
            
            # Convertir Decimales a float para JSON
            resultado_convertido = convertir_decimales(resultado)
            
            return JsonResponse(resultado_convertido)
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'mensaje': f'Error al procesar el análisis: {str(e)}'
            })


@method_decorator(require_http_methods(["POST"]), name='dispatch')
class AnalisisHorizontalResultadosView(LoginRequiredMixin, View):
    """
    Vista para generar análisis horizontal del Estado de Resultados.
    """
    
    def post(self, request):
        try:
            # Obtener datos del POST
            empresa_id = request.POST.get('empresa_id')
            años_seleccionados = request.POST.getlist('años[]')
            
            # Validar datos
            if not empresa_id:
                return JsonResponse({
                    'success': False,
                    'mensaje': 'Debe seleccionar una empresa.'
                })
            
            if not años_seleccionados or len(años_seleccionados) < 2:
                return JsonResponse({
                    'success': False,
                    'mensaje': 'Se necesitan al menos 2 años para realizar el análisis horizontal.'
                })
            
            # Obtener empresa
            try:
                empresa = Empresa.objects.get(id=empresa_id)
            except Empresa.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'mensaje': 'La empresa seleccionada no existe.'
                })
            
            # Convertir años a enteros y ordenar
            años = sorted([int(año) for año in años_seleccionados])
            
            # Realizar análisis horizontal
            resultado = AnalizadorHorizontal.analizar_estado_resultados(empresa, años)
            
            if resultado.get('error'):
                return JsonResponse({
                    'success': False,
                    'mensaje': resultado['error']
                })
            
            # Convertir Decimales a float para JSON
            resultado_convertido = convertir_decimales(resultado)
            
            return JsonResponse(resultado_convertido)
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'mensaje': f'Error al procesar el análisis: {str(e)}'
            })


@method_decorator(require_http_methods(["POST"]), name='dispatch')
class AnalisisVerticalBalanceView(LoginRequiredMixin, View):
    """
    Vista para generar análisis vertical del Balance General.
    Calcula % sobre Activo Total.
    """
    
    def post(self, request):
        try:
            # Obtener datos del POST
            empresa_id = request.POST.get('empresa_id')
            años_seleccionados = request.POST.getlist('años[]')
            
            # Validar datos
            if not empresa_id:
                return JsonResponse({
                    'success': False,
                    'mensaje': 'Debe seleccionar una empresa.'
                })
            
            if not años_seleccionados:
                return JsonResponse({
                    'success': False,
                    'mensaje': 'Debe seleccionar al menos un año.'
                })
            
            # Obtener empresa
            try:
                empresa = Empresa.objects.get(id=empresa_id)
            except Empresa.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'mensaje': 'La empresa seleccionada no existe.'
                })
            
            # Convertir años a enteros y ordenar
            años = sorted([int(año) for año in años_seleccionados])
            
            # Realizar análisis vertical
            resultado = AnalizadorVertical.analizar_balance_general(empresa, años)
            
            if resultado.get('error'):
                return JsonResponse({
                    'success': False,
                    'mensaje': resultado['error']
                })
            
            # Convertir Decimales a float para JSON
            resultado_convertido = convertir_decimales(resultado)
            
            return JsonResponse(resultado_convertido)
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'mensaje': f'Error al procesar el análisis: {str(e)}'
            })


@method_decorator(require_http_methods(["POST"]), name='dispatch')
class AnalisisVerticalResultadosView(LoginRequiredMixin, View):
    """
    Vista para generar análisis vertical del Estado de Resultados.
    Calcula % sobre Ingresos/Ventas Totales.
    """
    
    def post(self, request):
        try:
            # Obtener datos del POST
            empresa_id = request.POST.get('empresa_id')
            años_seleccionados = request.POST.getlist('años[]')
            
            # Validar datos
            if not empresa_id:
                return JsonResponse({
                    'success': False,
                    'mensaje': 'Debe seleccionar una empresa.'
                })
            
            if not años_seleccionados:
                return JsonResponse({
                    'success': False,
                    'mensaje': 'Debe seleccionar al menos un año.'
                })
            
            # Obtener empresa
            try:
                empresa = Empresa.objects.get(id=empresa_id)
            except Empresa.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'mensaje': 'La empresa seleccionada no existe.'
                })
            
            # Convertir años a enteros y ordenar
            años = sorted([int(año) for año in años_seleccionados])
            
            # Realizar análisis vertical
            resultado = AnalizadorVertical.analizar_estado_resultados(empresa, años)
            
            if resultado.get('error'):
                return JsonResponse({
                    'success': False,
                    'mensaje': resultado['error']
                })
            
            # Convertir Decimales a float para JSON
            resultado_convertido = convertir_decimales(resultado)
            
            return JsonResponse(resultado_convertido)
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'mensaje': f'Error al procesar el análisis: {str(e)}'
            })