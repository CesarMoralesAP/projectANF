from django.db import models
from apps.core.models import ModeloBase
from apps.empresas.models import Empresa


class TipoCuenta(models.TextChoices):
    """
    Tipos de cuentas contables.
    """
    ACTIVO = 'ACTIVO', 'Activo'
    PASIVO = 'PASIVO', 'Pasivo'
    PATRIMONIO = 'PATRIMONIO', 'Patrimonio'
    INGRESO = 'INGRESO', 'Ingreso'
    GASTO = 'GASTO', 'Gasto'
    RESULTADO = 'RESULTADO', 'Resultado'


class CatalogoCuenta(ModeloBase):
    """
    Modelo para el catálogo de cuentas contables de una empresa.
    Una empresa tiene un solo catálogo de cuentas.
    """
    empresa = models.OneToOneField(
        Empresa,
        on_delete=models.CASCADE,
        related_name='catalogo_cuenta',
        verbose_name='Empresa'
    )
    
    class Meta:
        db_table = 'catalogo_cuenta'
        verbose_name = 'Catálogo de Cuentas'
        verbose_name_plural = 'Catálogos de Cuentas'
        ordering = ['-creado_en']
    
    def __str__(self):
        return f'Catálogo de {self.empresa.nombre}'


class CuentaContable(ModeloBase):
    """
    Modelo para las cuentas contables dentro de un catálogo.
    """
    catalogo = models.ForeignKey(
        CatalogoCuenta,
        on_delete=models.CASCADE,
        related_name='cuentas',
        verbose_name='Catálogo'
    )
    codigo = models.CharField(
        max_length=20,
        verbose_name='Código de la cuenta',
        help_text='Ejemplo: 0101'
    )
    nombre = models.CharField(
        max_length=200,
        verbose_name='Nombre de la cuenta',
        help_text='Ejemplo: Activos corrientes'
    )
    tipo = models.CharField(
        max_length=20,
        choices=TipoCuenta.choices,
        verbose_name='Tipo de cuenta'
    )
    
    class Meta:
        db_table = 'cuenta_contable'
        verbose_name = 'Cuenta Contable'
        verbose_name_plural = 'Cuentas Contables'
        ordering = ['codigo', 'nombre']
        unique_together = [['catalogo', 'codigo']]
    
    def __str__(self):
        return f'{self.codigo} - {self.nombre}'


class RatioFinanciero(ModeloBase):
    """
    Modelo para los ratios financieros predefinidos.
    Estos ratios son globales y aplicables a cualquier empresa.
    """
    nombre = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Nombre del ratio',
        help_text='Ejemplo: Razón Corriente, ROE, ROA'
    )
    formula_display = models.CharField(
        max_length=255,
        verbose_name='Fórmula',
        help_text='Ejemplo: Activo Corriente / Pasivo Corriente'
    )
    categoria = models.CharField(
        max_length=50,
        verbose_name='Categoría',
        help_text='Ejemplo: Liquidez, Endeudamiento, Rentabilidad'
    )
    
    class Meta:
        db_table = 'ratio_financiero'
        verbose_name = 'Ratio Financiero'
        verbose_name_plural = 'Ratios Financieros'
        ordering = ['categoria', 'nombre']
    
    def __str__(self):
        return f'{self.nombre} ({self.categoria})'


class ComponenteRatio(ModeloBase):
    """
    Modelo para los componentes genéricos que forman parte de la fórmula de un ratio financiero.
    Por ejemplo, para "Razón Corriente", los componentes son "Activo Corriente" y "Pasivo Corriente".
    """
    ratio_financiero = models.ForeignKey(
        RatioFinanciero,
        on_delete=models.CASCADE,
        related_name='componentes',
        verbose_name='Ratio Financiero'
    )
    nombre_componente = models.CharField(
        max_length=100,
        verbose_name='Nombre del componente',
        help_text='Ejemplo: Activo Corriente, Utilidad Neta, Patrimonio'
    )
    
    class Meta:
        db_table = 'componente_ratio'
        verbose_name = 'Componente de Ratio'
        verbose_name_plural = 'Componentes de Ratios'
        ordering = ['ratio_financiero', 'nombre_componente']
        unique_together = [['ratio_financiero', 'nombre_componente']]
    
    def __str__(self):
        return f'{self.ratio_financiero.nombre} - {self.nombre_componente}'


class MapeoCuentaRatio(ModeloBase):
    """
    Modelo para mapear cuentas contables específicas de una empresa a componentes de ratios financieros.
    Este mapeo es específico por empresa (catálogo de cuentas).
    """
    catalogo_cuenta = models.ForeignKey(
        CatalogoCuenta,
        on_delete=models.CASCADE,
        related_name='mapeos_ratios',
        verbose_name='Catálogo de Cuentas'
    )
    componente_ratio = models.ForeignKey(
        ComponenteRatio,
        on_delete=models.CASCADE,
        related_name='mapeos_cuentas',
        verbose_name='Componente de Ratio'
    )
    cuenta_contable = models.ForeignKey(
        CuentaContable,
        on_delete=models.CASCADE,
        related_name='mapeos_ratios',
        verbose_name='Cuenta Contable',
        null=True,
        blank=True
    )
    
    class Meta:
        db_table = 'mapeo_cuenta_ratio'
        verbose_name = 'Mapeo de Cuenta a Ratio'
        verbose_name_plural = 'Mapeos de Cuentas a Ratios'
        ordering = ['catalogo_cuenta', 'componente_ratio']
        unique_together = [['catalogo_cuenta', 'componente_ratio']]
    
    def clean(self):
        """
        Valida que la cuenta contable pertenezca al mismo catálogo de cuentas.
        Permite que cuenta_contable sea null (campo en blanco).
        """
        from django.core.exceptions import ValidationError
        if self.cuenta_contable and self.catalogo_cuenta:
            if self.cuenta_contable.catalogo != self.catalogo_cuenta:
                raise ValidationError({
                    'cuenta_contable': 'La cuenta contable debe pertenecer al mismo catálogo de cuentas.'
                })
    
    def save(self, *args, **kwargs):
        """
        Ejecuta la validación antes de guardar.
        """
        self.full_clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        if self.cuenta_contable:
            return f'{self.catalogo_cuenta.empresa.nombre} - {self.componente_ratio.nombre_componente} → {self.cuenta_contable.codigo}'
        else:
            return f'{self.catalogo_cuenta.empresa.nombre} - {self.componente_ratio.nombre_componente} → (sin mapear)'
