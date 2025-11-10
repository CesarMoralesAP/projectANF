"""
URL configuration for ProjectANF project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # Redirigir la raíz al login
    path('', include('apps.usuarios.urls')),
    path('empresas/', include('apps.empresas.urls')),
    path('catalogos/', include('apps.catalogos.urls')),
    path('parametros/', include('apps.parametros.urls')),
    path('estados/', include('apps.estados.urls')),
    # path('analisis/', include('apps.analisis.urls')),
    # path('proyecciones/', include('apps.proyecciones.urls')),
    # path('graficas/', include('apps.graficas.urls')),
]

# Servir archivos estáticos y media en desarrollo
if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
