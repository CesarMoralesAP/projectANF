from django.db import models


class Sector(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    valor_referencia = models.JSONField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sector'

    def __str__(self):
        return self.nombre


class Empresa(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=150)
    sector = models.ForeignKey(Sector, models.DO_NOTHING, db_column='sector_id', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'empresa'

    def __str__(self):
        return self.nombre


class Catalogo(models.Model):
    id = models.AutoField(primary_key=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    estructura = models.JSONField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'catalogo'

    def __str__(self):
        return f"Catálogo de {self.empresa}"


class Cuenta(models.Model):
    id = models.AutoField(primary_key=True)
    catalogo = models.ForeignKey(Catalogo, on_delete=models.CASCADE)
    codigo = models.CharField(max_length=50, blank=True, null=True)
    nombre = models.CharField(max_length=100, blank=True, null=True)
    tipo = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cuenta'

    def __str__(self):
        return f"{self.codigo or ''} - {self.nombre or ''}"


class DatosFinancieros(models.Model):
    id = models.AutoField(primary_key=True)
    cuenta = models.ForeignKey(Cuenta, models.DO_NOTHING, db_column='cuenta_id', blank=True, null=True)
    anio = models.PositiveSmallIntegerField(blank=True, null=True)
    valor = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'datos_financieros'

    def __str__(self):
        return f"{self.cuenta} ({self.anio})"


class RatioFinanciero(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    formula = models.TextField(blank=True, null=True)
    valor_objetivo_sector = models.JSONField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ratio_financiero'

    def __str__(self):
        return self.nombre


class ResultadoRatio(models.Model):
    id = models.AutoField(primary_key=True)
    empresa = models.ForeignKey(Empresa, models.DO_NOTHING, db_column='empresa_id', blank=True, null=True)
    ratio = models.ForeignKey(RatioFinanciero, models.DO_NOTHING, db_column='ratio_id', blank=True, null=True)
    anio = models.PositiveSmallIntegerField(blank=True, null=True)
    valor = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    cumple_sector = models.BooleanField(blank=True, null=True)
    cumple_promedio = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'resultado_ratio'

    def __str__(self):
        return f"{self.empresa} - {self.ratio}"


class Informe(models.Model):
    id = models.AutoField(primary_key=True)
    empresa = models.ForeignKey(Empresa, models.DO_NOTHING, db_column='empresa_id', blank=True, null=True)
    anio = models.PositiveSmallIntegerField(blank=True, null=True)
    tipo = models.CharField(max_length=50, blank=True, null=True)
    contenido = models.JSONField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'informe'

    def __str__(self):
        return f"Informe {self.tipo or ''} - {self.empresa or ''} ({self.anio or ''})"
