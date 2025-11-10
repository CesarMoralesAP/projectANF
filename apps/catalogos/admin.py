from django.contrib import admin
from .models import CatalogoCuenta, CuentaContable


@admin.register(CatalogoCuenta)
class CatalogoCuentaAdmin(admin.ModelAdmin):
    list_display = ['empresa', 'creado_en', 'actualizado_en']
    list_filter = ['creado_en', 'actualizado_en']
    search_fields = ['empresa__nombre']
    readonly_fields = ['creado_en', 'actualizado_en']


@admin.register(CuentaContable)
class CuentaContableAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre', 'tipo', 'catalogo', 'creado_en']
    list_filter = ['tipo', 'catalogo', 'creado_en']
    search_fields = ['codigo', 'nombre', 'catalogo__empresa__nombre']
    readonly_fields = ['creado_en', 'actualizado_en']
