from django.urls import path
from . import views

app_name = 'analisis'

urlpatterns = [
    # Vista principal de Informes y Análisis
    path(
        '',
        views.InformesAnalisisView.as_view(),
        name='informes_lista'
    ),
    
    # Historial de proyecciones
    path(
        'historial/',
        views.HistorialProyeccionesView.as_view(),
        name='historial_proyecciones'
    ),
    
    # Selección de método de proyección
    path(
        'empresa/<int:empresa_id>/proyeccion/',
        views.ProyeccionMetodosView.as_view(),
        name='proyeccion_metodos'
    ),
    
    # Subir proyección desde Excel
    path(
        'empresa/<int:empresa_id>/proyeccion/subir/',
        views.SubirProyeccionView.as_view(),
        name='subir_proyeccion'
    ),
    
    # Calcular proyección desde base de datos
    path(
        'empresa/<int:empresa_id>/proyeccion/calcular/',
        views.CalcularProyeccionView.as_view(),
        name='calcular_proyeccion'
    ),
    
    # Ver gráfico de proyección
    path(
        'proyeccion/<int:pk>/grafico/',
        views.GraficoProyeccionView.as_view(),
        name='ver_grafico'
    ),
    
    # Eliminar proyección (solo superusuarios)
    path(
        'proyeccion/<int:pk>/eliminar/',
        views.EliminarProyeccionView.as_view(),
        name='eliminar_proyeccion'
    ),
]

