from django.db import models
from django.core.exceptions import ValidationError
from apps.core.models import ModeloBase
from apps.empresas.models import Empresa
from apps.catalogos.models import RatioFinanciero


class ValorRatioCalculado(ModeloBase):
    """
    Almacena los valores calculados de ratios financieros por empresa y año.
    Permite histórico de cálculos y comparaciones entre períodos.
    """
    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.CASCADE,
        related_name='valores_ratios',
        verbose_name='Empresa'
    )
    ratio = models.ForeignKey(
        RatioFinanciero,
        on_delete=models.CASCADE,
        related_name='valores_calculados',
        verbose_name='Ratio Financiero'
    )
    año = models.PositiveIntegerField(
        verbose_name='Año'
    )
    valor_calculado = models.DecimalField(
        max_digits=15,
        decimal_places=4,
        null=True,
        blank=True,
        verbose_name='Valor Calculado',
        help_text='Valor del ratio calculado para este año'
    )
    
    # Parámetros de referencia al momento del cálculo (para histórico)
    parametro_sectorial = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        null=True,
        blank=True,
        verbose_name='Parámetro Sectorial',
        help_text='Valor óptimo sectorial al momento del cálculo'
    )
    promedio_sector = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        null=True,
        blank=True,
        verbose_name='Promedio del Sector',
        help_text='Promedio sectorial al momento del cálculo'
    )
    promedio_general = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        null=True,
        blank=True,
        verbose_name='Promedio General',
        help_text='Promedio general al momento del cálculo'
    )
    
    # Comparaciones
    superior_parametro_sectorial = models.BooleanField(
        default=False,
        verbose_name='Superior al Parámetro Sectorial'
    )
    superior_promedio_sector = models.BooleanField(
        default=False,
        verbose_name='Superior al Promedio del Sector'
    )
    superior_promedio_general = models.BooleanField(
        default=False,
        verbose_name='Superior al Promedio General'
    )
    
    # Metadatos del cálculo
    fecha_calculo = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Cálculo'
    )
    usuario_calculo = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Usuario que Generó el Cálculo'
    )
    
    class Meta:
        db_table = 'valor_ratio_calculado'
        verbose_name = 'Valor de Ratio Calculado'
        verbose_name_plural = 'Valores de Ratios Calculados'
        unique_together = [['empresa', 'ratio', 'año']]
        ordering = ['empresa', 'ratio', '-año']
        indexes = [
            models.Index(fields=['empresa', 'año']),
            models.Index(fields=['ratio', 'año']),
        ]
    
    def __str__(self):
        return f"{self.ratio.nombre} - {self.empresa.nombre} ({self.año}): {self.valor_calculado}"
    
    def clean(self):
        """
        Validaciones del modelo.
        """
        if self.año < 1900 or self.año > 2100:
            raise ValidationError('El año debe estar entre 1900 y 2100')
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

