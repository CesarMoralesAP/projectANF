from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.views import View
from django.urls import reverse
from django.db import transaction
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
from apps.empresas.models import Sector
from apps.catalogos.models import RatioFinanciero
from .models import RatioReferenciaSector
from collections import defaultdict


class ParametrosSectorialesView(LoginRequiredMixin, TemplateView):
    """
    Vista principal para gestionar parámetros sectoriales (valores de referencia de ratios).
    """
    template_name = 'parametros/parametros_sectoriales.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Obtener todos los sectores con el conteo de ratios configurados
        sectores = Sector.objects.all().order_by('nombre')
        sectores_con_conteo = []
        
        for sector in sectores:
            ratios_configurados = RatioReferenciaSector.objects.filter(
                sector=sector
            ).exclude(valor_optimo__isnull=True).count()
            
            sectores_con_conteo.append({
                'sector': sector,
                'ratios_configurados': ratios_configurados
            })
        
        context['sectores_con_conteo'] = sectores_con_conteo
        
        # Obtener sector seleccionado
        sector_id = self.request.GET.get('sector')
        sector_seleccionado = None
        valores_referencia = {}
        
        if sector_id:
            try:
                sector_seleccionado = get_object_or_404(Sector, pk=sector_id)
                
                # Obtener todos los valores de referencia para este sector
                referencias = RatioReferenciaSector.objects.filter(
                    sector=sector_seleccionado
                ).select_related('ratio_financiero')
                
                # Crear diccionario: ratio_id -> valor_optimo
                # Solo incluir valores que no sean None y que no sean cadenas vacías
                for referencia in referencias:
                    if referencia.valor_optimo is not None and referencia.valor_optimo != '':
                        valores_referencia[referencia.ratio_financiero.id] = str(referencia.valor_optimo)
            
            except Exception as e:
                messages.error(self.request, f'Error al cargar el sector: {str(e)}')
        
        # Obtener ratios financieros agrupados por categoría
        ratios_por_categoria = defaultdict(list)
        ratios = RatioFinanciero.objects.all().order_by('categoria', 'nombre')
        
        for ratio in ratios:
            ratios_por_categoria[ratio.categoria].append(ratio)
        
        context['sector_seleccionado'] = sector_seleccionado
        context['ratios_por_categoria'] = dict(ratios_por_categoria)
        context['valores_referencia'] = valores_referencia
        
        return context


@method_decorator(require_http_methods(["POST"]), name='dispatch')
class GuardarParametrosSectorView(LoginRequiredMixin, View):
    """
    Vista para guardar los valores de referencia de ratios para un sector.
    """
    def post(self, request):
        sector_id = request.POST.get('sector_id')
        if not sector_id:
            messages.error(request, 'No se especificó el sector.')
            return redirect('parametros:parametros_sectoriales')
        
        sector = get_object_or_404(Sector, pk=sector_id)
        
        try:
            with transaction.atomic():
                # Obtener todos los ratios financieros
                ratios = RatioFinanciero.objects.all()
                
                ratios_creados = 0
                ratios_actualizados = 0
                ratios_eliminados = 0
                
                # Procesar cada ratio
                for ratio in ratios:
                    campo_name = f'ratio_{ratio.id}'
                    valor_str = request.POST.get(campo_name, '').strip()
                    
                    # Intentar obtener la referencia existente
                    try:
                        referencia = RatioReferenciaSector.objects.get(
                            sector=sector,
                            ratio_financiero=ratio
                        )
                        referencia_existia = True
                    except RatioReferenciaSector.DoesNotExist:
                        referencia = None
                        referencia_existia = False
                    
                    if valor_str:
                        try:
                            valor_optimo = float(valor_str)
                            
                            # Crear o actualizar referencia
                            if referencia_existia:
                                # La referencia ya existe, actualizarla si cambió el valor
                                valor_actual = referencia.valor_optimo if referencia.valor_optimo is not None else None
                                if valor_actual != valor_optimo:
                                    referencia.valor_optimo = valor_optimo
                                    referencia.save()
                                    ratios_actualizados += 1
                            else:
                                # Crear nueva referencia
                                RatioReferenciaSector.objects.create(
                                    sector=sector,
                                    ratio_financiero=ratio,
                                    valor_optimo=valor_optimo
                                )
                                ratios_creados += 1
                        except ValueError:
                            messages.warning(
                                request,
                                f'El valor para "{ratio.nombre}" no es válido. Se omitió.'
                            )
                    else:
                        # Si el campo está vacío, eliminar la referencia si existe
                        if referencia_existia:
                            referencia.delete()
                            ratios_eliminados += 1
                
                # Mensaje de éxito
                total_cambios = ratios_creados + ratios_actualizados + ratios_eliminados
                if total_cambios > 0:
                    mensaje = f'Parámetros guardados exitosamente para el sector "{sector.nombre}". '
                    partes = []
                    if ratios_creados > 0:
                        partes.append(f'{ratios_creados} creado(s)')
                    if ratios_actualizados > 0:
                        partes.append(f'{ratios_actualizados} actualizado(s)')
                    if ratios_eliminados > 0:
                        partes.append(f'{ratios_eliminados} eliminado(s)')
                    mensaje += ', '.join(partes) + '.'
                    messages.success(request, mensaje)
                else:
                    messages.info(request, 'No se realizaron cambios en los parámetros.')
        
        except Exception as e:
            messages.error(request, f'Error al guardar los parámetros: {str(e)}')
        
        return redirect(reverse('parametros:parametros_sectoriales') + f'?sector={sector_id}')
