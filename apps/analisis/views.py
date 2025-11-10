from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, CreateView, DetailView, ListView, DeleteView
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils import timezone
from apps.empresas.models import Empresa
from apps.core.mixins import PermisoEliminarMixin
from .models import ProyeccionFinanciera, OrigenDatos
from .forms import SubirProyeccionForm
from .utils import procesar_excel_proyeccion, validar_estructura_excel
import os


class InformesAnalisisView(LoginRequiredMixin, ListView):
    """
    Vista principal de Informes y Análisis.
    Muestra lista de empresas con botón para acceder a proyecciones.
    """
    model = Empresa
    template_name = 'analisis/informes_lista.html'
    context_object_name = 'empresas'
    
    def get_queryset(self):
        return Empresa.objects.select_related('sector').order_by('nombre')


class ProyeccionMetodosView(LoginRequiredMixin, TemplateView):
    """
    Vista para seleccionar el método de generación de proyección.
    Muestra opciones: Subir Excel o Calcular en la app.
    """
    template_name = 'analisis/proyeccion_metodos.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        empresa_id = self.kwargs.get('empresa_id')
        context['empresa'] = get_object_or_404(Empresa, pk=empresa_id)
        return context


class CalcularProyeccionView(LoginRequiredMixin, TemplateView):
    """
    Vista para calcular proyección desde datos de la base de datos.
    Lee valores históricos de Mes y Venta de la tabla del sistema.
    
    NOTA: Esta vista está preparada para cuando se defina la tabla
    de ventas históricas. Por ahora usa datos de referencia.
    """
    template_name = 'analisis/proyeccion_calculada.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        empresa_id = self.kwargs.get('empresa_id')
        context['empresa'] = get_object_or_404(Empresa, pk=empresa_id)
        return context
    
    def post(self, request, *args, **kwargs):
        """
        Calcula la proyección usando datos históricos del sistema.
        """
        empresa_id = self.kwargs.get('empresa_id')
        empresa = get_object_or_404(Empresa, pk=empresa_id)
        
        try:
            # TODO: Cuando se defina la tabla de ventas, reemplazar esta consulta
            # Ejemplo de consulta futura:
            # datos_historicos = VentaMensual.objects.filter(empresa=empresa).order_by('periodo')
            # datos = [{'mes': v.periodo.strftime('%B %Y'), 'venta': float(v.valor_venta)} 
            #          for v in datos_historicos]
            
            # Por ahora, obtener datos de referencia (PLACEHOLDER)
            datos_historicos = self._obtener_datos_historicos(empresa)
            
            if not datos_historicos:
                messages.error(
                    request,
                    'No se encontraron datos históricos de ventas para esta empresa.'
                )
                return redirect('analisis:proyeccion_metodos', empresa_id=empresa_id)
            
            # Calcular proyecciones usando los 3 métodos
            datos_proyeccion = self._calcular_proyecciones(datos_historicos)
            
            # Crear y guardar la proyección
            nombre_proyeccion = f"Proyección {empresa.nombre} - {timezone.now().strftime('%d/%m/%Y')}"
            
            proyeccion = ProyeccionFinanciera.objects.create(
                empresa=empresa,
                nombre=nombre_proyeccion,
                descripcion="Proyección calculada automáticamente desde datos del sistema",
                origen=OrigenDatos.CALCULADO,
                datos_grafico=datos_proyeccion
            )
            
            messages.success(
                request,
                f'Proyección calculada exitosamente para {empresa.nombre}'
            )
            return redirect('analisis:ver_grafico', pk=proyeccion.pk)
            
        except Exception as e:
            messages.error(
                request,
                f'Error al calcular proyección: {str(e)}'
            )
            return redirect('analisis:proyeccion_metodos', empresa_id=empresa_id)
    
    def _obtener_datos_historicos(self, empresa):
        """
        Obtiene datos históricos de ventas de la base de datos.
        
        TODO: Reemplazar con consulta real cuando se defina la tabla.
        
        Estructura esperada de la tabla futura:
        - Columna: mes/periodo (DateField o CharField)
        - Columna: venta/valor (DecimalField)
        
        Returns:
            list: [{'mes': 'Enero 2024', 'venta': 1000.00}, ...]
        """
        # PLACEHOLDER - Datos de ejemplo para desarrollo
        # Cuando se cree la tabla real, descomentar y usar esta consulta:
        
        """
        # Opción 1: Si la tabla tiene campos 'periodo' y 'valor_venta'
        from apps.TU_APP.models import VentaMensual  # TODO: Reemplazar con modelo real
        
        ventas = VentaMensual.objects.filter(
            empresa=empresa
        ).order_by('periodo').values('periodo', 'valor_venta')
        
        return [
            {
                'mes': venta['periodo'].strftime('%B %Y'),  # Si es DateField
                'venta': float(venta['valor_venta'])
            }
            for venta in ventas
        ]
        """
        
        # Por ahora retornar lista vacía para indicar que falta implementar
        return []
    
    def _calcular_proyecciones(self, datos_historicos):
        """
        Calcula las proyecciones usando los 3 métodos.
        
        Args:
            datos_historicos: [{'mes': 'Enero', 'venta': 1000}, ...]
        
        Returns:
            dict: Estructura igual al procesador de Excel
        """
        # Extraer periodos y valores
        periodos = [d['mes'] for d in datos_historicos]
        valores = [d['venta'] for d in datos_historicos]
        
        # TODO: Implementar cálculos matemáticos reales
        # Por ahora, estructura básica de retorno
        
        return {
            'valor_incremental': {
                'periodos': periodos,
                'valores': valores  # TODO: Aplicar fórmula de valor incremental
            },
            'valor_absoluto': {
                'periodos': periodos,
                'valores': valores  # TODO: Aplicar fórmula de valor absoluto
            },
            'minimos_cuadrados': {
                'periodos': periodos,
                'valores': valores  # TODO: Aplicar fórmula de mínimos cuadrados
            }
        }


class SubirProyeccionView(LoginRequiredMixin, CreateView):
    """
    Vista para subir archivo Excel con proyecciones.
    Procesa el archivo y guarda los datos en JSON.
    """
    model = ProyeccionFinanciera
    form_class = SubirProyeccionForm
    template_name = 'analisis/proyeccion_upload.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        empresa_id = self.kwargs.get('empresa_id')
        context['empresa'] = get_object_or_404(Empresa, pk=empresa_id)
        return context
    
    def form_valid(self, form):
        """
        Procesa el archivo Excel y guarda la proyección.
        """
        empresa_id = self.kwargs.get('empresa_id')
        empresa = get_object_or_404(Empresa, pk=empresa_id)
        
        # Guardar proyección
        proyeccion = form.save(commit=False)
        proyeccion.empresa = empresa
        proyeccion.origen = OrigenDatos.ARCHIVO
        proyeccion.save()
        
        try:
            # Validar estructura del Excel
            es_valido, mensaje = validar_estructura_excel(proyeccion.archivo.path)
            
            if not es_valido:
                proyeccion.delete()
                messages.error(self.request, f'Error en estructura del archivo: {mensaje}')
                return redirect('analisis:subir_proyeccion', empresa_id=empresa_id)
            
            # Procesar Excel
            datos_procesados = procesar_excel_proyeccion(proyeccion.archivo.path)
            
            # Guardar datos procesados
            proyeccion.datos_grafico = datos_procesados
            proyeccion.save()
            
            messages.success(
                self.request,
                f'Proyección "{proyeccion.nombre}" procesada exitosamente.'
            )
            return redirect('analisis:ver_grafico', pk=proyeccion.pk)
        
        except Exception as e:
            # Si hay error, eliminar la proyección
            proyeccion.delete()
            messages.error(
                self.request,
                f'Error al procesar archivo: {str(e)}'
            )
            return redirect('analisis:subir_proyeccion', empresa_id=empresa_id)
    
    def form_invalid(self, form):
        """
        Maneja errores de validación del formulario.
        """
        messages.error(
            self.request,
            'Por favor, corrija los errores en el formulario.'
        )
        return super().form_invalid(form)


class HistorialProyeccionesView(LoginRequiredMixin, ListView):
    """
    Vista para mostrar historial de proyecciones guardadas.
    """
    model = ProyeccionFinanciera
    template_name = 'analisis/historial_proyecciones.html'
    context_object_name = 'proyecciones'
    paginate_by = 10
    
    def get_queryset(self):
        return ProyeccionFinanciera.objects.select_related('empresa', 'empresa__sector').order_by('-creado_en')


class GraficoProyeccionView(LoginRequiredMixin, DetailView):
    """
    Vista para visualizar el gráfico de proyección.
    Muestra ambos métodos (valor incremental y valor absoluto).
    """
    model = ProyeccionFinanciera
    template_name = 'analisis/proyeccion_grafico.html'
    context_object_name = 'proyeccion'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        proyeccion = self.get_object()
        
        # Pasar datos del gráfico al template
        context['datos_grafico'] = proyeccion.datos_grafico
        context['empresa'] = proyeccion.empresa
        
        return context


class EliminarProyeccionView(PermisoEliminarMixin, LoginRequiredMixin, DeleteView):
    """
    Vista para eliminar una proyección financiera.
    Solo accesible para superusuarios.
    """
    model = ProyeccionFinanciera
    success_url = reverse_lazy('analisis:historial_proyecciones')
    
    def delete(self, request, *args, **kwargs):
        """
        Elimina la proyección y muestra mensaje de confirmación.
        """
        proyeccion = self.get_object()
        nombre_proyeccion = proyeccion.nombre
        
        # Eliminar archivo si existe
        if proyeccion.archivo:
            try:
                if os.path.isfile(proyeccion.archivo.path):
                    os.remove(proyeccion.archivo.path)
            except Exception:
                pass  # Continuar aunque falle la eliminación del archivo
        
        messages.success(
            self.request,
            f'La proyección "{nombre_proyeccion}" ha sido eliminada exitosamente.'
        )
        return super().delete(request, *args, **kwargs)

