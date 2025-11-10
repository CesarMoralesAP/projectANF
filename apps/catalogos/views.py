from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.views import View
from django.urls import reverse
from django.db import transaction
from apps.empresas.models import Empresa
from .models import CatalogoCuenta, CuentaContable, TipoCuenta, RatioFinanciero, ComponenteRatio, MapeoCuentaRatio
from .forms import CuentaContableForm, CargarExcelForm
from .utils import generar_plantilla_excel, procesar_excel
from collections import defaultdict


class CatalogoContableView(LoginRequiredMixin, TemplateView):
    """
    Vista para mostrar el selector de empresas y gestionar catálogos contables.
    """
    template_name = 'catalogos/catalogo_lista.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtener empresas con sus sectores
        context['empresas'] = Empresa.objects.select_related('sector').all().order_by('nombre')
        
        # Obtener empresa seleccionada
        empresa_id = self.request.GET.get('empresa')
        empresa_seleccionada = None
        catalogo = None
        cuentas = []
        
        if empresa_id:
            try:
                empresa_seleccionada = get_object_or_404(
                    Empresa.objects.select_related('sector'),
                    pk=empresa_id
                )
                # Obtener o crear el catálogo para la empresa
                catalogo, creado = CatalogoCuenta.objects.get_or_create(
                    empresa=empresa_seleccionada
                )
                # Obtener cuentas del catálogo
                cuentas = catalogo.cuentas.all().order_by('codigo', 'nombre')
            except Exception as e:
                messages.error(self.request, f'Error al cargar la empresa: {str(e)}')
        
        context['empresa_seleccionada'] = empresa_seleccionada
        context['catalogo'] = catalogo
        context['cuentas'] = cuentas
        context['tipos_cuenta'] = TipoCuenta.choices
        context['form_cuenta'] = CuentaContableForm()
        context['form_excel'] = CargarExcelForm()
        
        # Obtener ratios financieros agrupados por categoría
        ratios_por_categoria = defaultdict(list)
        ratios = RatioFinanciero.objects.prefetch_related('componentes').all().order_by('categoria', 'nombre')
        
        for ratio in ratios:
            ratios_por_categoria[ratio.categoria].append(ratio)
        
        context['ratios_por_categoria'] = dict(ratios_por_categoria)
        
        # Obtener mapeos existentes para el catálogo (si existe)
        # Crear un diccionario con claves como strings para acceso fácil en templates
        mapeos_existentes = {}
        if catalogo:
            mapeos = MapeoCuentaRatio.objects.filter(
                catalogo_cuenta=catalogo
            ).select_related('componente_ratio', 'cuenta_contable')
            
            # Crear diccionario: str(componente_ratio_id) -> cuenta_contable_id
            for mapeo in mapeos:
                if mapeo.cuenta_contable:
                    mapeos_existentes[str(mapeo.componente_ratio.id)] = mapeo.cuenta_contable.id
        
        context['mapeos_existentes'] = mapeos_existentes
        
        return context


class DescargarPlantillaView(LoginRequiredMixin, View):
    """
    Vista para descargar la plantilla Excel.
    """
    def get(self, request):
        output = generar_plantilla_excel()
        response = HttpResponse(
            output.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=plantilla_cuentas_contables.xlsx'
        return response


@method_decorator(require_http_methods(["POST"]), name='dispatch')
class CargarExcelView(LoginRequiredMixin, View):
    """
    Vista para cargar y procesar un archivo Excel con cuentas contables.
    """
    def post(self, request):
        empresa_id = request.POST.get('empresa_id')
        if not empresa_id:
            messages.error(request, 'No se especificó la empresa.')
            return redirect('catalogos:catalogo_lista')
        
        empresa = get_object_or_404(Empresa, pk=empresa_id)
        catalogo, creado = CatalogoCuenta.objects.get_or_create(empresa=empresa)
        
        form = CargarExcelForm(request.POST, request.FILES)
        if form.is_valid():
            archivo = request.FILES['archivo']
            cuentas_creadas, errores = procesar_excel(archivo, catalogo)
            
            if errores:
                for error in errores:
                    messages.warning(request, error)
            
            if cuentas_creadas > 0:
                messages.success(
                    request,
                    f'Catálogo cargado exitosamente. Se procesaron {cuentas_creadas} cuenta(s) contable(s).'
                )
            elif not errores:
                messages.info(request, 'No se encontraron cuentas para procesar en el archivo.')
        else:
            messages.error(request, 'Por favor, seleccione un archivo Excel válido.')
        
        return redirect(reverse('catalogos:catalogo_lista') + f'?empresa={empresa_id}')


@method_decorator(require_http_methods(["POST"]), name='dispatch')
class AgregarCuentaView(LoginRequiredMixin, View):
    """
    Vista para agregar una cuenta contable manualmente.
    """
    def post(self, request):
        empresa_id = request.POST.get('empresa_id')
        if not empresa_id:
            return JsonResponse({'success': False, 'error': 'No se especificó la empresa.'}, status=400)
        
        empresa = get_object_or_404(Empresa, pk=empresa_id)
        catalogo, creado = CatalogoCuenta.objects.get_or_create(empresa=empresa)
        
        form = CuentaContableForm(request.POST, catalogo=catalogo)
        if form.is_valid():
            cuenta = form.save(commit=False)
            cuenta.catalogo = catalogo
            cuenta.save()
            return JsonResponse({
                'success': True,
                'message': 'Cuenta agregada correctamente.',
                'cuenta': {
                    'id': cuenta.id,
                    'codigo': cuenta.codigo,
                    'nombre': cuenta.nombre,
                    'tipo': cuenta.get_tipo_display(),
                }
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            }, status=400)


@method_decorator(require_http_methods(["DELETE", "POST"]), name='dispatch')
class EliminarCuentaView(LoginRequiredMixin, View):
    """
    Vista para eliminar una cuenta contable.
    """
    def post(self, request, cuenta_id):
        cuenta = get_object_or_404(CuentaContable, pk=cuenta_id)
        empresa_id = cuenta.catalogo.empresa.id
        cuenta.delete()
        messages.success(request, 'Cuenta eliminada correctamente.')
        return redirect(reverse('catalogos:catalogo_lista') + f'?empresa={empresa_id}')


@method_decorator(require_http_methods(["POST"]), name='dispatch')
class GuardarMapeosView(LoginRequiredMixin, View):
    """
    Vista para guardar todos los mapeos de cuentas a ratios financieros de una vez.
    """
    def post(self, request):
        empresa_id = request.POST.get('empresa_id')
        if not empresa_id:
            messages.error(request, 'No se especificó la empresa.')
            return redirect('catalogos:catalogo_lista')
        
        empresa = get_object_or_404(Empresa, pk=empresa_id)
        catalogo, creado = CatalogoCuenta.objects.get_or_create(empresa=empresa)
        
        try:
            with transaction.atomic():
                # Obtener todos los componentes de ratios
                componentes = ComponenteRatio.objects.all()
                
                mapeos_creados = 0
                mapeos_actualizados = 0
                mapeos_eliminados = 0
                
                # Procesar cada componente
                for componente in componentes:
                    campo_name = f'mapeo_{componente.id}'
                    cuenta_id = request.POST.get(campo_name, '').strip()
                    
                    # Intentar obtener el mapeo existente
                    try:
                        mapeo = MapeoCuentaRatio.objects.get(
                            catalogo_cuenta=catalogo,
                            componente_ratio=componente
                        )
                        mapeo_existia = True
                    except MapeoCuentaRatio.DoesNotExist:
                        mapeo = None
                        mapeo_existia = False
                    
                    if cuenta_id:
                        # Validar que la cuenta pertenezca al catálogo
                        try:
                            cuenta = CuentaContable.objects.get(
                                pk=cuenta_id,
                                catalogo=catalogo
                            )
                            
                            # Crear o actualizar mapeo
                            if mapeo_existia:
                                # El mapeo ya existe, actualizarlo solo si cambió la cuenta
                                cuenta_actual_id = mapeo.cuenta_contable.id if mapeo.cuenta_contable else None
                                if cuenta_actual_id != cuenta.id:
                                    mapeo.cuenta_contable = cuenta
                                    mapeo.save()
                                    mapeos_actualizados += 1
                            else:
                                # Crear nuevo mapeo
                                MapeoCuentaRatio.objects.create(
                                    catalogo_cuenta=catalogo,
                                    componente_ratio=componente,
                                    cuenta_contable=cuenta
                                )
                                mapeos_creados += 1
                        except CuentaContable.DoesNotExist:
                            messages.warning(
                                request,
                                f'La cuenta seleccionada para "{componente.nombre_componente}" no pertenece a este catálogo.'
                            )
                    else:
                        # Si el campo está vacío, eliminar el mapeo si existe
                        if mapeo_existia:
                            mapeo.delete()
                            mapeos_eliminados += 1
                        # Si no existía, no hay nada que hacer
                
                # Mensaje de éxito
                total_cambios = mapeos_creados + mapeos_actualizados + mapeos_eliminados
                if total_cambios > 0:
                    mensaje = f'Mapeos guardados exitosamente. '
                    partes = []
                    if mapeos_creados > 0:
                        partes.append(f'{mapeos_creados} creado(s)')
                    if mapeos_actualizados > 0:
                        partes.append(f'{mapeos_actualizados} actualizado(s)')
                    if mapeos_eliminados > 0:
                        partes.append(f'{mapeos_eliminados} eliminado(s)')
                    mensaje += ', '.join(partes) + '.'
                    messages.success(request, mensaje)
                else:
                    messages.info(request, 'No se realizaron cambios en los mapeos.')
        
        except Exception as e:
            messages.error(request, f'Error al guardar los mapeos: {str(e)}')
        
        return redirect(reverse('catalogos:catalogo_lista') + f'?empresa={empresa_id}')
