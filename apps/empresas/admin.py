from django.contrib import admin
from .models import Sector, Empresa


@admin.register(Sector)
class SectorAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'creado_en']
    list_filter = ['creado_en']
    search_fields = ['nombre']


@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'sector']
    list_filter = ['sector', 'creado_en']
    search_fields = ['nombre']
    autocomplete_fields = ['sector']

