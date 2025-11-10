from django.db import models
from apps.core.models import ModeloBase


class RatioReferenciaSector(ModeloBase):
    """
    Modelo para almacenar los valores de referencia (óptimos) para cada ratio financiero según el sector.
    Estos valores se utilizarán para comparaciones y análisis en el módulo de Parámetros Sectoriales.
    """
    ratio_financiero = models.ForeignKey(
        'catalogos.RatioFinanciero',
        on_delete=models.CASCADE,
        related_name='referencias_sector',
        verbose_name='Ratio Financiero'
    )
    sector = models.ForeignKey(
        'empresas.Sector',
        on_delete=models.CASCADE,
        related_name='ratios_referencia',
        verbose_name='Sector'
    )
    valor_optimo = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        null=True,
        blank=True,
        verbose_name='Valor Óptimo',
        help_text='Valor de referencia óptimo para este ratio en el sector'
    )
    promedio_sector = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        null=True,
        blank=True,
        verbose_name='Promedio del Sector',
        help_text='Ratio promedio de las empresas clasificadas en este sector'
    )
    
    class Meta:
        db_table = 'ratio_referencia_sector'
        verbose_name = 'Referencia de Ratio por Sector'
        verbose_name_plural = 'Referencias de Ratios por Sector'
        ordering = ['ratio_financiero__categoria', 'ratio_financiero__nombre']
        unique_together = [['ratio_financiero', 'sector']]
    
    def __str__(self):
        return f'{self.ratio_financiero.nombre} - {self.sector.nombre}: {self.valor_optimo or "N/A"}'

