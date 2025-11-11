from django.contrib import admin
from .models import Ventas, ProyeccionVenta


@admin.register(Ventas)
class VentasAdmin(admin.ModelAdmin):
    list_display = ['empresa', 'anio', 'mes', 'valor', 'creado_en']
    list_filter = ['empresa', 'anio']
    search_fields = ['empresa__nombre']
    ordering = ['-anio', '-mes']
    date_hierarchy = 'creado_en'


@admin.register(ProyeccionVenta)
class ProyeccionVentaAdmin(admin.ModelAdmin):
    list_display = ['empresa', 'anio', 'mes', 'metodo', 'valor_proyectado', 'creado_en']
    list_filter = ['empresa', 'metodo', 'anio']
    search_fields = ['empresa__nombre', 'metodo']
    ordering = ['-anio', '-mes']
    date_hierarchy = 'creado_en'
