from django.contrib import admin
from .models import EstadoFinanciero, ItemEstadoFinanciero


class ItemEstadoFinancieroInline(admin.TabularInline):
    """
    Inline para mostrar items dentro del estado financiero en el admin.
    """
    model = ItemEstadoFinanciero
    extra = 0
    fields = ['cuenta_contable', 'monto']
    readonly_fields = ['creado_en', 'actualizado_en']


@admin.register(EstadoFinanciero)
class EstadoFinancieroAdmin(admin.ModelAdmin):
    list_display = ['empresa', 'año', 'tipo', 'cantidad_cuentas', 'creado_en', 'actualizado_en']
    list_filter = ['tipo', 'año', 'creado_en', 'empresa']
    search_fields = ['empresa__nombre', 'año']
    readonly_fields = ['creado_en', 'actualizado_en']
    inlines = [ItemEstadoFinancieroInline]
    
    fieldsets = (
        ('Información General', {
            'fields': ('empresa', 'año', 'tipo')
        }),
        ('Auditoría', {
            'fields': ('creado_en', 'actualizado_en'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ItemEstadoFinanciero)
class ItemEstadoFinancieroAdmin(admin.ModelAdmin):
    list_display = ['estado_financiero', 'cuenta_contable', 'monto', 'creado_en']
    list_filter = ['estado_financiero__tipo', 'estado_financiero__año', 'estado_financiero__empresa', 'creado_en']
    search_fields = [
        'estado_financiero__empresa__nombre',
        'cuenta_contable__codigo',
        'cuenta_contable__nombre'
    ]
    readonly_fields = ['creado_en', 'actualizado_en']
    
    fieldsets = (
        ('Información del Item', {
            'fields': ('estado_financiero', 'cuenta_contable', 'monto')
        }),
        ('Auditoría', {
            'fields': ('creado_en', 'actualizado_en'),
            'classes': ('collapse',)
        }),
    )
