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
