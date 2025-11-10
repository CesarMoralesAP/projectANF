from django.contrib import admin
from .models import RatioReferenciaSector


@admin.register(RatioReferenciaSector)
class RatioReferenciaSectorAdmin(admin.ModelAdmin):
    list_display = ['ratio_financiero', 'sector', 'valor_optimo', 'creado_en']
    list_filter = ['sector', 'ratio_financiero__categoria', 'creado_en']
    search_fields = ['ratio_financiero__nombre', 'sector__nombre']
    readonly_fields = ['creado_en', 'actualizado_en']

