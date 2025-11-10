from django.db import models
from django.core.exceptions import ValidationError
from apps.core.models import ModeloBase
from apps.empresas.models import Empresa
from apps.catalogos.models import CuentaContable


class TipoEstadoFinanciero(models.TextChoices):
    """
    Tipos de estados financieros.
    """
    BALANCE_GENERAL = 'BALANCE_GENERAL', 'Balance General'
    ESTADO_RESULTADOS = 'ESTADO_RESULTADOS', 'Estado de Resultados'


class EstadoFinanciero(ModeloBase):
    """
    Modelo para representar un estado financiero de una empresa en un año específico.
    Solo puede haber un estado financiero por empresa, año y tipo.
    """
    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.CASCADE,
        related_name='estados_financieros',
        verbose_name='Empresa'
    )
    año = models.IntegerField(
        verbose_name='Año',
        help_text='Año del estado financiero'
    )
    tipo = models.CharField(
        max_length=20,
        choices=TipoEstadoFinanciero.choices,
        verbose_name='Tipo de Estado Financiero'
    )
    
    class Meta:
        db_table = 'estado_financiero'
        verbose_name = 'Estado Financiero'
        verbose_name_plural = 'Estados Financieros'
        ordering = ['-año', 'tipo', 'empresa']
        unique_together = [['empresa', 'año', 'tipo']]
        indexes = [
            models.Index(fields=['empresa', 'año', 'tipo']),
        ]
    
    def clean(self):
        """
        Valida que no exista otro estado financiero con la misma empresa, año y tipo.
        """
        if self.empresa and self.año and self.tipo:
            queryset = EstadoFinanciero.objects.filter(
                empresa=self.empresa,
                año=self.año,
                tipo=self.tipo
            )
            if self.pk:
                queryset = queryset.exclude(pk=self.pk)
            if queryset.exists():
                raise ValidationError(
                    f'Ya existe un {self.get_tipo_display()} para {self.empresa.nombre} en el año {self.año}.'
                )
    
    def save(self, *args, **kwargs):
        """
        Ejecuta la validación antes de guardar.
        """
        self.full_clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.empresa.nombre} - {self.get_tipo_display()} - {self.año}'
    
    @property
    def cantidad_cuentas(self):
        """Retorna la cantidad de cuentas registradas en este estado."""
        return self.items.count()


class ItemEstadoFinanciero(ModeloBase):
    """
    Modelo para representar un item (cuenta con monto) dentro de un estado financiero.
    Solo puede haber un item por cuenta en un estado financiero.
    """
    estado_financiero = models.ForeignKey(
        EstadoFinanciero,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Estado Financiero'
    )
    cuenta_contable = models.ForeignKey(
        CuentaContable,
        on_delete=models.CASCADE,
        related_name='items_estados',
        verbose_name='Cuenta Contable'
    )
    monto = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        verbose_name='Monto',
        help_text='Monto de la cuenta en el estado financiero'
    )
    
    class Meta:
        db_table = 'item_estado_financiero'
        verbose_name = 'Item de Estado Financiero'
        verbose_name_plural = 'Items de Estados Financieros'
        ordering = ['cuenta_contable__codigo', 'cuenta_contable__nombre']
        unique_together = [['estado_financiero', 'cuenta_contable']]
        indexes = [
            models.Index(fields=['estado_financiero', 'cuenta_contable']),
        ]
    
    def clean(self):
        """
        Valida que la cuenta contable pertenezca al catálogo de la empresa del estado financiero.
        """
        if self.estado_financiero and self.cuenta_contable:
            if self.cuenta_contable.catalogo.empresa != self.estado_financiero.empresa:
                raise ValidationError(
                    'La cuenta contable debe pertenecer al catálogo de cuentas de la empresa del estado financiero.'
                )
    
    def save(self, *args, **kwargs):
        """
        Ejecuta la validación antes de guardar.
        """
        self.full_clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.estado_financiero} - {self.cuenta_contable.codigo} - {self.monto}'
