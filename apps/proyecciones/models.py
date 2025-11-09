from django.db import models
from apps.estados.models import Empresa


class Ventas(models.Model):
    """
    Tabla de ventas históricas por empresa, año y mes.
    """
    id = models.AutoField(primary_key=True)
    empresa = models.ForeignKey(Empresa, models.DO_NOTHING, db_column='empresa_id', blank=True, null=True)
    anio = models.PositiveSmallIntegerField(blank=True, null=True)
    mes = models.PositiveSmallIntegerField(blank=True, null=True)
    valor = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ventas'

    def __str__(self):
        return f"{self.empresa} - {self.mes}/{self.anio}: {self.valor}"


class ProyeccionVenta(models.Model):
    """
    Tabla de proyecciones de ventas generadas por métodos estadísticos.
    """
    id = models.AutoField(primary_key=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    anio = models.PositiveSmallIntegerField(blank=True, null=True)
    mes = models.PositiveSmallIntegerField(blank=True, null=True)
    metodo = models.CharField(max_length=50, blank=True, null=True)
    valor_proyectado = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'proyeccion_ventas'

    def __str__(self):
        return f"{self.empresa} - {self.metodo} ({self.mes}/{self.anio})"
