from django.urls import path
from apps.graficos_financieros import views  # Actualizado al nuevo nombre

app_name = 'graficas'

urlpatterns = [
    # Vista principal de Gráficos
    path(
        '',
        views.InformesAnalisisView.as_view(),
        name='graficos_lista'
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
    
    # === RATIOS FINANCIEROS ===
    
    # Análisis de ratios por empresa
    path(
        'empresa/<int:empresa_id>/ratios/',
        views.RatiosEmpresaView.as_view(),
        name='ratios_empresa'
    ),
    
    # Historial de análisis de ratios
    path(
        'historial-ratios/',
        views.HistorialRatiosView.as_view(),
        name='historial_ratios'
    ),
    
    # Ver gráfico de ratios
    path(
        'ratios/<int:pk>/grafico/',
        views.VerRatiosView.as_view(),
        name='ver_ratios'
    ),
    
    # Eliminar análisis de ratios (solo superusuarios)
    path(
        'ratios/<int:pk>/eliminar/',
        views.EliminarRatioView.as_view(),
        name='eliminar_ratio'
    ),
]

