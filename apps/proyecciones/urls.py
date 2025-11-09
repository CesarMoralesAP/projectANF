from django.urls import path
from . import views

urlpatterns = [
    path('proyecciones/', views.cargar_proyeccion, name='cargar_proyeccion'),
]