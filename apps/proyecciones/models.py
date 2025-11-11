from django.db import models
from apps.core.models import ModeloBase
from apps.empresas.models import Empresa


class Ventas(ModeloBase):
    """
    Tabla de ventas históricas por empresa, año y mes.
    """
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, db_column='empresa_id')
    anio = models.PositiveSmallIntegerField()
    mes = models.PositiveSmallIntegerField()
    valor = models.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        db_table = 'ventas'
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'
        ordering = ['empresa', 'anio', 'mes']
        unique_together = [['empresa', 'anio', 'mes']]

    def __str__(self):
        return f"{self.empresa} - {self.mes}/{self.anio}: {self.valor}"


class ProyeccionVenta(ModeloBase):
    """
    Tabla de proyecciones de ventas generadas por métodos estadísticos.
    """
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    anio = models.PositiveSmallIntegerField()
    mes = models.PositiveSmallIntegerField()
    metodo = models.CharField(max_length=50)
    valor_proyectado = models.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        db_table = 'proyeccion_ventas'
        verbose_name = 'Proyección de Venta'
        verbose_name_plural = 'Proyecciones de Ventas'
        ordering = ['empresa', 'anio', 'mes']

    def __str__(self):
        return f"{self.empresa} - {self.metodo} ({self.mes}/{self.anio})"
