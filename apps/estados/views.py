from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.views import View
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.db import transaction
from datetime import datetime
from apps.empresas.models import Empresa
from apps.catalogos.models import CatalogoCuenta, CuentaContable, TipoCuenta
from .models import EstadoFinanciero, ItemEstadoFinanciero, TipoEstadoFinanciero
from .forms import EstadoFinancieroForm, CargarExcelEstadoForm
from .servicios.generar_plantilla_excel_estado import generar_plantilla_excel_estado
from .servicios.procesar_excel_estado import procesar_excel_estado
from collections import defaultdict


class EstadoFinancieroView(LoginRequiredMixin, TemplateView):
    """
    Vista principal para gestionar estados financieros.
    Muestra el selector de empresa, año y tipo, y la lista de estados guardados.
    """
    template_name = 'estados/estado_financiero.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Obtener empresas
        context['empresas'] = Empresa.objects.select_related('sector').all().order_by('nombre')
        
        # Obtener parámetros de la URL
        empresa_id = self.request.GET.get('empresa')
        año = self.request.GET.get('año')
        tipo = self.request.GET.get('tipo')
        estado_id = self.request.GET.get('estado_id')  # Para edición
        
        empresa_seleccionada = None
        catalogo = None
        cuentas_por_tipo = defaultdict(list)
        estado_existente = None
        items_existentes = {}  # Diccionario: {cuenta_id: monto}
        
        # Si hay empresa seleccionada
        if empresa_id:
            try:
                empresa_seleccionada = get_object_or_404(Empresa, pk=empresa_id)
                
                # Obtener catálogo
                try:
                    catalogo = CatalogoCuenta.objects.get(empresa=empresa_seleccionada)
                except CatalogoCuenta.DoesNotExist:
                    catalogo = None
                    messages.warning(
                        self.request,
                        f'La empresa "{empresa_seleccionada.nombre}" no tiene un catálogo de cuentas configurado.'
                    )
                
                # Si hay año y tipo, obtener cuentas y estado existente
                if año and tipo:
                    año_int = int(año)
                    tipo_str = str(tipo).strip()
                    
                    # Valores válidos de tipos de estado
                    BALANCE_GENERAL_VAL = TipoEstadoFinanciero.BALANCE_GENERAL
                    ESTADO_RESULTADOS_VAL = TipoEstadoFinanciero.ESTADO_RESULTADOS
                    
                    # Intentar obtener estado existente
                    try:
                        estado_existente = EstadoFinanciero.objects.get(
                            empresa=empresa_seleccionada,
                            año=año_int,
                            tipo=tipo_str
                        )
                        # Obtener items existentes
                        items = estado_existente.items.select_related('cuenta_contable').all()
                        for item in items:
                            # Convertir Decimal a float para que se muestre correctamente en el template
                            items_existentes[item.cuenta_contable.id] = float(item.monto)
                    except EstadoFinanciero.DoesNotExist:
                        estado_existente = None
                    
                    # Filtrar cuentas según el tipo de estado
                    if tipo_str == BALANCE_GENERAL_VAL:
                        tipos_cuenta = [TipoCuenta.ACTIVO, TipoCuenta.PASIVO, TipoCuenta.PATRIMONIO]
                    elif tipo_str == ESTADO_RESULTADOS_VAL:
                        tipos_cuenta = [TipoCuenta.INGRESO, TipoCuenta.GASTO, TipoCuenta.RESULTADO]
                    else:
                        tipos_cuenta = []
                        # Obtener valores válidos para el mensaje
                        valores_validos = [TipoEstadoFinanciero.BALANCE_GENERAL, TipoEstadoFinanciero.ESTADO_RESULTADOS]
                        messages.warning(
                            self.request, 
                            f'Tipo de estado financiero no válido: "{tipo_str}". Valores válidos: {", ".join(valores_validos)}'
                        )
                    
                    if catalogo and tipos_cuenta:
                        # Verificar que el catálogo tenga cuentas
                        total_cuentas = catalogo.cuentas.count()
                        if total_cuentas == 0:
                            messages.info(self.request, f'El catálogo de la empresa "{empresa_seleccionada.nombre}" no tiene cuentas definidas.')
                        else:
                            # Obtener todas las cuentas para debugging
                            todas_las_cuentas = catalogo.cuentas.all()
                            tipos_en_catalogo = set(todas_las_cuentas.values_list('tipo', flat=True).distinct())
                            
                            # Filtrar cuentas por tipo
                            cuentas = catalogo.cuentas.filter(tipo__in=tipos_cuenta).order_by('codigo', 'nombre')
                            cantidad_cuentas_filtradas = cuentas.count()
                            
                            if cantidad_cuentas_filtradas == 0:
                                # Crear diccionario de tipos para obtener labels
                                tipos_dict = dict(TipoCuenta.choices)
                                tipos_buscados_labels = [tipos_dict.get(t, t) for t in tipos_cuenta]
                                tipos_disponibles_labels = [tipos_dict.get(t, t) for t in tipos_en_catalogo]
                                messages.warning(
                                    self.request,
                                    f'No se encontraron cuentas de tipo {", ".join(tipos_buscados_labels)} '
                                    f'en el catálogo. Tipos disponibles en el catálogo: {", ".join(tipos_disponibles_labels) if tipos_disponibles_labels else "Ninguno"}.'
                                )
                            else:
                                # Agrupar cuentas por tipo
                                for cuenta in cuentas:
                                    monto = items_existentes.get(cuenta.id, 0.00)
                                    cuentas_por_tipo[cuenta.get_tipo_display()].append({
                                        'id': cuenta.id,
                                        'codigo': cuenta.codigo,
                                        'nombre': cuenta.nombre,
                                        'tipo': cuenta.get_tipo_display(),
                                        'monto': monto
                                    })
            except Exception as e:
                messages.error(self.request, f'Error al cargar los datos: {str(e)}')
        
        # Obtener todos los estados financieros guardados
        estados_guardados = EstadoFinanciero.objects.select_related('empresa').prefetch_related('items').all().order_by('-año', 'tipo', 'empresa')
        
        context['empresa_seleccionada'] = empresa_seleccionada
        context['catalogo'] = catalogo
        context['año_seleccionado'] = año
        context['tipo_seleccionado'] = tipo
        context['cuentas_por_tipo'] = dict(cuentas_por_tipo)
        context['estado_existente'] = estado_existente
        context['estados_guardados'] = estados_guardados
        context['tipos_estado'] = TipoEstadoFinanciero.choices
        context['año_actual'] = datetime.now().year
        
        return context


@method_decorator(require_http_methods(["GET"]), name='dispatch')
class DescargarPlantillaEstadoView(LoginRequiredMixin, View):
    """
    Vista para descargar la plantilla Excel personalizada según empresa y tipo de estado.
    """
    def get(self, request):
        empresa_id = request.GET.get('empresa')
        tipo_estado = request.GET.get('tipo')
        
        if not empresa_id or not tipo_estado:
            messages.error(request, 'Debe seleccionar una empresa y un tipo de estado.')
            return redirect('estados:estado_financiero')
        
        empresa = get_object_or_404(Empresa, pk=empresa_id)
        
        try:
            catalogo = CatalogoCuenta.objects.get(empresa=empresa)
        except CatalogoCuenta.DoesNotExist:
            messages.error(request, f'La empresa "{empresa.nombre}" no tiene un catálogo de cuentas configurado.')
            return redirect('estados:estado_financiero')
        
        try:
            output = generar_plantilla_excel_estado(catalogo, tipo_estado)
            
            # Nombre del archivo
            tipo_nombre = 'Balance_General' if tipo_estado == TipoEstadoFinanciero.BALANCE_GENERAL else 'Estado_Resultados'
            filename = f'plantilla_{tipo_nombre}_{empresa.nombre}_{datetime.now().year}.xlsx'
            
            response = HttpResponse(
                output.getvalue(),
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = f'attachment; filename={filename}'
            return response
        except Exception as e:
            messages.error(request, f'Error al generar la plantilla: {str(e)}')
            return redirect('estados:estado_financiero')


@method_decorator(require_http_methods(["POST"]), name='dispatch')
class GuardarEstadoFinancieroView(LoginRequiredMixin, View):
    """
    Vista para guardar un estado financiero desde ingreso manual.
    """
    def post(self, request):
        empresa_id = request.POST.get('empresa_id')
        año = request.POST.get('año')
        tipo = request.POST.get('tipo')
        
        if not empresa_id or not año or not tipo:
            return JsonResponse({
                'success': False,
                'error': 'Faltan datos requeridos (empresa, año, tipo).'
            }, status=400)
        
        try:
            empresa = get_object_or_404(Empresa, pk=empresa_id)
            año_int = int(año)
            
            # Verificar que existe catálogo
            try:
                catalogo = CatalogoCuenta.objects.get(empresa=empresa)
            except CatalogoCuenta.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'error': f'La empresa "{empresa.nombre}" no tiene un catálogo de cuentas configurado.'
                }, status=400)
            
            # Filtrar tipos de cuenta según el tipo de estado
            if tipo == TipoEstadoFinanciero.BALANCE_GENERAL:
                tipos_cuenta = [TipoCuenta.ACTIVO, TipoCuenta.PASIVO, TipoCuenta.PATRIMONIO]
            elif tipo == TipoEstadoFinanciero.ESTADO_RESULTADOS:
                tipos_cuenta = [TipoCuenta.INGRESO, TipoCuenta.GASTO, TipoCuenta.RESULTADO]
            else:
                return JsonResponse({
                    'success': False,
                    'error': 'Tipo de estado financiero no válido.'
                }, status=400)
            
            # Obtener cuentas válidas
            cuentas = catalogo.cuentas.filter(tipo__in=tipos_cuenta)
            cuenta_ids = set(cuentas.values_list('id', flat=True))
            
            # Procesar con transacción atómica
            with transaction.atomic():
                # Obtener o crear estado financiero
                estado_financiero, creado = EstadoFinanciero.objects.get_or_create(
                    empresa=empresa,
                    año=año_int,
                    tipo=tipo,
                    defaults={}
                )
                
                # Si ya existía, eliminar items existentes
                if not creado:
                    ItemEstadoFinanciero.objects.filter(estado_financiero=estado_financiero).delete()
                
                # Procesar items del formulario
                items_creados = 0
                for key, value in request.POST.items():
                    if key.startswith('monto_'):
                        cuenta_id = int(key.replace('monto_', ''))
                        
                        # Validar que la cuenta pertenece al catálogo y tipo correcto
                        if cuenta_id not in cuenta_ids:
                            continue
                        
                        try:
                            cuenta = CuentaContable.objects.get(pk=cuenta_id, catalogo=catalogo)
                            # Convertir el valor a float, si está vacío o es None, usar 0.00
                            monto_str = value.strip() if value else '0.00'
                            monto = float(monto_str) if monto_str else 0.00
                            
                            # Guardar el item siempre, incluso si el monto es 0.00
                            # Esto permite que el usuario pueda "limpiar" valores estableciéndolos en 0
                            ItemEstadoFinanciero.objects.create(
                                estado_financiero=estado_financiero,
                                cuenta_contable=cuenta,
                                monto=monto
                            )
                            items_creados += 1
                        except (CuentaContable.DoesNotExist, ValueError) as e:
                            continue
                
                # Redirigir a la misma página con los parámetros para mostrar los valores actualizados
                return JsonResponse({
                    'success': True,
                    'message': f'Estado financiero {"creado" if creado else "actualizado"} exitosamente. {items_creados} cuenta(s) registrada(s).',
                    'estado_id': estado_financiero.id,
                    'redirect_url': reverse('estados:estado_financiero') + f'?empresa={empresa.id}&año={año_int}&tipo={tipo}'
                })
        
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'Error al guardar el estado financiero: {str(e)}'
            }, status=500)


@method_decorator(require_http_methods(["POST"]), name='dispatch')
class CargarExcelEstadoView(LoginRequiredMixin, View):
    """
    Vista para cargar y procesar un archivo Excel con datos del estado financiero.
    """
    def post(self, request):
        empresa_id = request.POST.get('empresa_id')
        año = request.POST.get('año')
        tipo = request.POST.get('tipo')
        
        if not empresa_id or not año or not tipo:
            messages.error(request, 'Faltan datos requeridos (empresa, año, tipo).')
            return redirect('estados:estado_financiero')
        
        empresa = get_object_or_404(Empresa, pk=empresa_id)
        año_int = int(año)
        
        form = CargarExcelEstadoForm(request.POST, request.FILES)
        if form.is_valid():
            archivo = request.FILES['archivo']
            try:
                éxito, errores, items_procesados = procesar_excel_estado(archivo, empresa, año_int, tipo)
                
                # Mostrar errores si los hay
                if errores:
                    for error in errores:
                        messages.error(request, error)
                
                # Mostrar mensaje de éxito o advertencia
                if éxito:
                    messages.success(
                        request,
                        f'Estado financiero cargado exitosamente. Se procesaron {items_procesados} cuenta(s).'
                    )
                elif items_procesados > 0:
                    messages.warning(
                        request,
                        f'Se procesaron {items_procesados} cuenta(s), pero hubo algunos errores. Revise los mensajes de error arriba.'
                    )
                else:
                    if not errores:
                        messages.error(request, 'No se pudo procesar el archivo. No se encontraron datos válidos para procesar.')
                    # Si hay errores, ya se mostraron arriba
            except Exception as e:
                messages.error(request, f'Error al procesar el archivo Excel: {str(e)}')
                import traceback
                print(f"Error completo: {traceback.format_exc()}")
        else:
            # Mostrar errores del formulario
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Error en {field}: {error}')
            messages.error(request, 'Por favor, seleccione un archivo Excel válido.')
        
        return redirect(reverse('estados:estado_financiero') + f'?empresa={empresa_id}&año={año}&tipo={tipo}')


@method_decorator(require_http_methods(["GET"]), name='dispatch')
class EditarEstadoFinancieroView(LoginRequiredMixin, View):
    """
    Vista para cargar un estado financiero existente para edición.
    Redirige a la vista principal con los parámetros preseleccionados.
    """
    def get(self, request, estado_id):
        estado = get_object_or_404(EstadoFinanciero, pk=estado_id)
        
        # Redirigir a la vista principal con los parámetros
        return redirect(
            reverse('estados:estado_financiero') + 
            f'?empresa={estado.empresa.id}&año={estado.año}&tipo={estado.tipo}&estado_id={estado.id}'
        )


@method_decorator(require_http_methods(["POST", "DELETE"]), name='dispatch')
class EliminarEstadoFinancieroView(LoginRequiredMixin, View):
    """
    Vista para eliminar un estado financiero.
    """
    def post(self, request, estado_id):
        estado = get_object_or_404(EstadoFinanciero, pk=estado_id)
        empresa_id = estado.empresa.id
        año = estado.año
        tipo_display = estado.get_tipo_display()
        
        # Eliminar estado (los items se eliminan en cascada)
        estado.delete()
        
        messages.success(
            request,
            f'{tipo_display} del año {año} eliminado exitosamente.'
        )
        
        return redirect(reverse('estados:estado_financiero') + f'?empresa={empresa_id}')


@method_decorator(require_http_methods(["GET"]), name='dispatch')
class VerEstadoFinancieroView(LoginRequiredMixin, View):
    """
    Vista para ver los detalles de un estado financiero.
    Retorna JSON con los datos del estado.
    """
    def get(self, request, estado_id):
        estado = get_object_or_404(
            EstadoFinanciero.objects.select_related('empresa').prefetch_related('items__cuenta_contable'),
            pk=estado_id
        )
        
        # Agrupar items por tipo de cuenta
        items_por_tipo = defaultdict(list)
        for item in estado.items.all():
            items_por_tipo[item.cuenta_contable.get_tipo_display()].append({
                'codigo': item.cuenta_contable.codigo,
                'nombre': item.cuenta_contable.nombre,
                'monto': float(item.monto)
            })
        
        return JsonResponse({
            'success': True,
            'estado': {
                'id': estado.id,
                'empresa': estado.empresa.nombre,
                'año': estado.año,
                'tipo': estado.get_tipo_display(),
                'cantidad_cuentas': estado.cantidad_cuentas,
                'items_por_tipo': dict(items_por_tipo)
            }
        })
