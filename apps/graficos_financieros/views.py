from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, CreateView, DetailView, ListView, DeleteView
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils import timezone
from apps.empresas.models import Empresa
from apps.core.mixins import PermisoEliminarMixin
from .models import ProyeccionFinanciera, OrigenDatos, AnalisisRatio
from apps.catalogos.models import RatioFinanciero
from apps.analisis.models import ValorRatioCalculado
from .forms import SubirProyeccionForm
from .utils import procesar_excel_proyeccion, validar_estructura_excel
import os


class InformesAnalisisView(LoginRequiredMixin, ListView):
    """
    Vista principal de Informes y Análisis.
    Muestra lista de empresas con botón para acceder a proyecciones.
    """
    model = Empresa
    template_name = 'graficos_financieros/informes_lista.html'
    context_object_name = 'empresas'
    
    def get_queryset(self):
        return Empresa.objects.select_related('sector').order_by('nombre')


class ProyeccionMetodosView(LoginRequiredMixin, TemplateView):
    """
    Vista para seleccionar el método de generación de proyección.
    Muestra opciones: Subir Excel o Calcular en la app.
    """
    template_name = 'graficos_financieros/proyeccion_metodos.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        empresa_id = self.kwargs.get('empresa_id')
        context['empresa'] = get_object_or_404(Empresa, pk=empresa_id)
        return context


class CalcularProyeccionView(LoginRequiredMixin, TemplateView):
    """
    Vista para calcular proyección desde la tabla proyeccion_ventas.
    
    Lee los datos con los 3 métodos ya calculados:
    - Incremento Porcentual
    - Incremento Absoluto
    - Mínimos Cuadrados
    
    Genera un gráfico con 3 líneas mostrando todos los años disponibles.
    """
    template_name = 'graficos_financieros/proyeccion_calculada.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        empresa_id = self.kwargs.get('empresa_id')
        context['empresa'] = get_object_or_404(Empresa, pk=empresa_id)
        return context
    
    def post(self, request, *args, **kwargs):
        """
        Calcula la proyección usando datos desde proyeccion_ventas.
        """
        empresa_id = self.kwargs.get('empresa_id')
        empresa = get_object_or_404(Empresa, pk=empresa_id)
        
        try:
            # Obtener datos históricos desde proyeccion_ventas
            datos_por_metodo = self._obtener_datos_historicos(empresa)
            
            # Validar que existan datos
            if not any(datos_por_metodo.values()):
                messages.error(
                    request,
                    'No se encontraron datos de proyección para esta empresa en la base de datos.'
                )
                return redirect('graficas:proyeccion_metodos', empresa_id=empresa_id)
            
            # Formatear para Chart.js (3 líneas)
            datos_proyeccion = self._calcular_proyecciones(datos_por_metodo)
            
            # Crear y guardar la proyección
            nombre_proyeccion = f"Proyección {empresa.nombre} - {timezone.now().strftime('%d/%m/%Y')}"
            
            proyeccion = ProyeccionFinanciera.objects.create(
                empresa=empresa,
                nombre=nombre_proyeccion,
                descripcion="Proyección calculada desde datos del sistema (3 métodos)",
                origen=OrigenDatos.CALCULADO,
                datos_grafico=datos_proyeccion
            )
            
            messages.success(
                request,
                f'Proyección calculada exitosamente para {empresa.nombre}'
            )
            return redirect('graficas:ver_grafico', pk=proyeccion.pk)
            
        except Exception as e:
            messages.error(
                request,
                f'Error al calcular proyección: {str(e)}'
            )
            return redirect('graficas:proyeccion_metodos', empresa_id=empresa_id)
    
    def _obtener_datos_historicos(self, empresa):
        """
        Obtiene datos históricos de proyecciones desde la tabla proyeccion_ventas.
        
        Lee los datos ya calculados con los 3 métodos:
        - Incremento Porcentual
        - Incremento Absoluto
        - Mínimos Cuadrados
        
        Returns:
            dict: {
                'Incremento Porcentual': [{'año': 2025, 'mes': 1, 'valor': 1000.00}, ...],
                'Incremento Absoluto': [...],
                'Mínimos Cuadrados': [...]
            }
        """
        from .models import ProyeccionVenta
        
        # Obtener todas las proyecciones de esta empresa
        proyecciones = ProyeccionVenta.objects.filter(
            empresa=empresa
        ).order_by('año', 'mes').values('año', 'mes', 'metodo', 'valor_proyectado')
        
        # Agrupar por método (incluyendo variaciones con/sin tilde)
        datos_por_metodo = {}
        
        for p in proyecciones:
            metodo = p['metodo']
            # Normalizar el nombre (agregar si no existe)
            if metodo not in datos_por_metodo:
                datos_por_metodo[metodo] = []
            
            datos_por_metodo[metodo].append({
                'año': p['año'],
                'mes': p['mes'],
                'valor': float(p['valor_proyectado'])
            })
        
        return datos_por_metodo
    
    def _calcular_proyecciones(self, datos_por_metodo):
        """
        Formatea las proyecciones al estilo Chart.js (igual que el Excel).
        
        Args:
            datos_por_metodo: {
                'Incremento Porcentual': [{'año': 2025, 'mes': 1, 'valor': 1000}, ...],
                ...
            }
        
        Returns:
            dict: Estructura para Chart.js con 3 líneas
        """
        # Mapeo de nombres de métodos (BD → Display)
        mapeo_metodos = {
            'Incremento Porcentual': 'valor_incremental',
            'Incremento Absoluto': 'valor_absoluto',
            'Mínimos Cuadrados': 'minimos_cuadrados',
            'Minimos Cuadrados': 'minimos_cuadrados'  # Sin tilde (como está en BD)
        }
        
        # Nombres de meses en español
        nombres_meses = [
            'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
            'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
        ]
        
        resultado = {}
        
        # Procesar cada método
        for metodo_bd, datos in datos_por_metodo.items():
            if not datos:
                continue
                
            metodo_display = mapeo_metodos.get(metodo_bd, metodo_bd.lower().replace(' ', '_'))
            
            # Crear etiquetas de periodos
            periodos = []
            valores = []
            
            for d in datos:
                año = d['año']
                mes_secuencial = d['mes']  # Este es un número de periodo secuencial (1-24)
                
                # Calcular el mes real del año
                # Si mes_secuencial > 12, es del año siguiente
                mes_real = ((mes_secuencial - 1) % 12) + 1
                año_real = año + ((mes_secuencial - 1) // 12)
                
                # Validar que el mes real esté en rango
                if mes_real < 1 or mes_real > 12:
                    periodos.append(f"Periodo {mes_secuencial} ({año_real})")
                else:
                    periodos.append(f"{nombres_meses[mes_real - 1]} {año_real}")
                
                valores.append(d['valor'])
            
            # Solo agregar si hay datos válidos
            if periodos and valores:
                resultado[metodo_display] = {
                    'periodos': periodos,
                    'valores': valores
                }
        
        return resultado


class SubirProyeccionView(LoginRequiredMixin, CreateView):
    """
    Vista para subir archivo Excel con proyecciones.
    Procesa el archivo y guarda los datos en JSON.
    """
    model = ProyeccionFinanciera
    form_class = SubirProyeccionForm
    template_name = 'graficos_financieros/proyeccion_upload.html'
    
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
                return redirect('graficas:subir_proyeccion', empresa_id=empresa_id)
            
            # Procesar Excel
            datos_procesados = procesar_excel_proyeccion(proyeccion.archivo.path)
            
            # Guardar datos procesados
            proyeccion.datos_grafico = datos_procesados
            proyeccion.save()
            
            messages.success(
                self.request,
                f'Proyección "{proyeccion.nombre}" procesada exitosamente.'
            )
            return redirect('graficas:ver_grafico', pk=proyeccion.pk)
        
        except Exception as e:
            # Si hay error, eliminar la proyección
            proyeccion.delete()
            messages.error(
                self.request,
                f'Error al procesar archivo: {str(e)}'
            )
            return redirect('graficas:subir_proyeccion', empresa_id=empresa_id)
    
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
    template_name = 'graficos_financieros/historial_proyecciones.html'
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
    template_name = 'graficos_financieros/proyeccion_grafico.html'
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
    success_url = reverse_lazy('graficas:historial_proyecciones')
    
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


# ============================================
# VISTAS DE RATIOS FINANCIEROS
# ============================================

class RatiosEmpresaView(LoginRequiredMixin, TemplateView):
    """
    Vista para mostrar y generar análisis de ratios de una empresa.
    Lee datos de valor_ratio_calculado y genera gráfico.
    """
    template_name = 'graficos_financieros/ratios_empresa.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        empresa_id = self.kwargs.get('empresa_id')
        empresa = get_object_or_404(Empresa, pk=empresa_id)
        
        context['empresa'] = empresa
        
        # Obtener todos los ratios disponibles
        ratios = RatioFinanciero.objects.all()
        context['ratios'] = ratios
        
        # Verificar si hay datos de ratios para esta empresa
        tiene_datos = ValorRatioCalculado.objects.filter(empresa=empresa).exists()
        context['tiene_datos'] = tiene_datos
        
        return context
    
    def post(self, request, *args, **kwargs):
        """
        Genera el análisis de ratios y lo guarda.
        """
        empresa_id = self.kwargs.get('empresa_id')
        empresa = get_object_or_404(Empresa, pk=empresa_id)
        
        try:
            # Obtener datos del formulario
            nombre_analisis = request.POST.get('nombre', '').strip()
            descripcion_analisis = request.POST.get('descripcion', '').strip()
            
            # Validar nombre
            if not nombre_analisis:
                messages.error(
                    request,
                    'Debe proporcionar un nombre para el análisis.'
                )
                return redirect('graficas:ratios_empresa', empresa_id=empresa_id)
            
            # Obtener datos de ratios de la empresa
            datos_grafico = self._obtener_datos_ratios(empresa)
            
            if not datos_grafico or not datos_grafico.get('años'):
                messages.error(
                    request,
                    'No se encontraron datos de ratios para esta empresa.'
                )
                return redirect('graficas:ratios_empresa', empresa_id=empresa_id)
            
            # Crear y guardar el análisis
            analisis = AnalisisRatio.objects.create(
                empresa=empresa,
                nombre=nombre_analisis,
                descripcion=descripcion_analisis if descripcion_analisis else f"Análisis de {len(datos_grafico['ratios'])} ratios financieros",
                datos_grafico=datos_grafico
            )
            
            messages.success(
                request,
                f'Análisis de ratios generado exitosamente para {empresa.nombre}'
            )
            return redirect('graficas:ver_ratios', pk=analisis.pk)
            
        except Exception as e:
            messages.error(
                request,
                f'Error al generar análisis: {str(e)}'
            )
            return redirect('graficas:ratios_empresa', empresa_id=empresa_id)
    
    def _obtener_datos_ratios(self, empresa):
        """
        Obtiene datos de ratios de la BD para graficar.
        
        Returns:
            dict: {
                'ratios': ['Razón Corriente', 'Prueba Ácida', ...],
                'años': [2022, 2023, 2024],
                'datos': {
                    'Razón Corriente': [0.26, 0.25, 0.25],
                    ...
                }
            }
        """
        # Obtener todos los valores de ratios de la empresa
        valores = ValorRatioCalculado.objects.filter(
            empresa=empresa
        ).select_related('ratio').order_by('ratio__nombre', 'año')
        
        if not valores:
            return {}
        
        # Extraer años únicos
        años = sorted(list(set(v.año for v in valores)))
        
        # Agrupar por ratio
        datos = {}
        ratios_nombres = []
        
        for valor in valores:
            ratio_nombre = valor.ratio.nombre
            if ratio_nombre not in datos:
                datos[ratio_nombre] = {}
                ratios_nombres.append(ratio_nombre)
            
            datos[ratio_nombre][valor.año] = float(valor.valor_calculado)
        
        # Convertir a formato para Chart.js
        datos_formateados = {}
        for ratio_nombre in ratios_nombres:
            datos_formateados[ratio_nombre] = [
                datos[ratio_nombre].get(año, None) for año in años
            ]
        
        return {
            'ratios': ratios_nombres,
            'años': años,
            'datos': datos_formateados
        }


class HistorialRatiosView(LoginRequiredMixin, ListView):
    """
    Vista para mostrar historial de análisis de ratios guardados.
    """
    model = AnalisisRatio
    template_name = 'graficos_financieros/historial_ratios.html'
    context_object_name = 'analisis_ratios'
    paginate_by = 10
    
    def get_queryset(self):
        return AnalisisRatio.objects.select_related('empresa', 'empresa__sector').order_by('-creado_en')


class VerRatiosView(LoginRequiredMixin, DetailView):
    """
    Vista para visualizar el gráfico de ratios guardado.
    """
    model = AnalisisRatio
    template_name = 'graficos_financieros/grafico_ratios.html'
    context_object_name = 'analisis'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        analisis = self.get_object()
        
        # Pasar datos del gráfico al template
        context['datos_grafico'] = analisis.datos_grafico
        context['empresa'] = analisis.empresa
        
        return context


class EliminarRatioView(PermisoEliminarMixin, LoginRequiredMixin, DeleteView):
    """
    Vista para eliminar un análisis de ratios.
    Solo accesible para superusuarios.
    """
    model = AnalisisRatio
    success_url = reverse_lazy('graficas:historial_ratios')
    
    def delete(self, request, *args, **kwargs):
        """
        Elimina el análisis y muestra mensaje de confirmación.
        """
        analisis = self.get_object()
        nombre_analisis = analisis.nombre
        
        messages.success(
            self.request,
            f'El análisis "{nombre_analisis}" ha sido eliminado exitosamente.'
        )
        return super().delete(request, *args, **kwargs)

