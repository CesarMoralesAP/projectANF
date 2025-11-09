from django.urls import path
from apps.estados.views import empresa_views

urlpatterns = [
    path('empresas/', empresa_views.listar_empresas, name='listar_empresas'),
    path('empresas/crear/', empresa_views.crear_empresa, name='crear_empresa'),
    path('empresas/editar/<int:id>/', empresa_views.editar_empresa, name='editar_empresa'),
    path('empresas/eliminar/<int:pk>/', empresa_views.eliminar_empresa, name='eliminar_empresa'),
]