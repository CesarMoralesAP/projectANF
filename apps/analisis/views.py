from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.views import View
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from apps.empresas.models import Empresa
from apps.analisis.servicios.validar_estados import ValidadorEstadosFinancieros


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
                return JsonResponse({
                    'success': True,
                    'mensaje': f'¡Análisis generado exitosamente para {empresa.nombre}!<br>Años analizados: {", ".join(map(str, años))}'
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

