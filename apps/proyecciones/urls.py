from django.urls import path
from . import views

app_name = 'proyecciones'

urlpatterns = [
    path('', views.ProyeccionVentasView.as_view(), name='proyeccion_ventas'),
    path('generar/', views.GenerarProyeccionView.as_view(), name='generar_proyeccion'),
]