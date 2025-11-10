from django.contrib import admin
from .models import CatalogoCuenta, CuentaContable, RatioFinanciero, ComponenteRatio, MapeoCuentaRatio


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


@admin.register(RatioFinanciero)
class RatioFinancieroAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'categoria', 'formula_display', 'creado_en']
    list_filter = ['categoria', 'creado_en']
    search_fields = ['nombre', 'formula_display', 'categoria']
    readonly_fields = ['creado_en', 'actualizado_en']


@admin.register(ComponenteRatio)
class ComponenteRatioAdmin(admin.ModelAdmin):
    list_display = ['ratio_financiero', 'nombre_componente', 'creado_en']
    list_filter = ['ratio_financiero__categoria', 'ratio_financiero', 'creado_en']
    search_fields = ['nombre_componente', 'ratio_financiero__nombre']
    readonly_fields = ['creado_en', 'actualizado_en']


@admin.register(MapeoCuentaRatio)
class MapeoCuentaRatioAdmin(admin.ModelAdmin):
    list_display = ['catalogo_cuenta', 'componente_ratio', 'cuenta_contable', 'creado_en']
    list_filter = ['catalogo_cuenta__empresa', 'componente_ratio__ratio_financiero__categoria', 'creado_en']
    search_fields = ['catalogo_cuenta__empresa__nombre', 'componente_ratio__nombre_componente', 'cuenta_contable__codigo']
    readonly_fields = ['creado_en', 'actualizado_en']
