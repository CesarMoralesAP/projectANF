from django.urls import path
from apps.estados.views import sector_views

urlpatterns = [
    path('sectores/', sector_views.listar_sectores, name='listar_sectores'),
    path('sectores/crear/', sector_views.crear_sector, name='crear_sector'),
    path('sectores/editar/<int:pk>/', sector_views.editar_sector, name='editar_sector'),
    path('sectores/eliminar/<int:pk>/', sector_views.eliminar_sector, name='eliminar_sector'),
]