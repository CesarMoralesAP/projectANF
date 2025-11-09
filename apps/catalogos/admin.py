from django.contrib import admin
from .models import Sector, Empresa


@admin.register(Sector)
class SectorAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion', 'activo', 'creado_en']
    list_filter = ['activo', 'creado_en']
    search_fields = ['nombre', 'descripcion']


@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'sector', 'nit', 'email', 'activo', 'creado_en']
    list_filter = ['sector', 'activo', 'creado_en']
    search_fields = ['nombre', 'nit', 'email']
    autocomplete_fields = ['sector']
