from django.db import models
from apps.core.models import ModeloBase


class Sector(ModeloBase):
    """
    Modelo para los sectores económicos de las empresas.
    """
    nombre = models.CharField(max_length=100, verbose_name='Nombre del sector')
    descripcion = models.TextField(blank=True, null=True, verbose_name='Descripción')
    
    class Meta:
        db_table = 'sector'
        verbose_name = 'Sector'
        verbose_name_plural = 'Sectores'
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre


class Empresa(ModeloBase):
    """
    Modelo para las empresas del sistema.
    """
    nombre = models.CharField(max_length=200, verbose_name='Nombre de la empresa')
    sector = models.ForeignKey(
        Sector,
        on_delete=models.PROTECT,
        related_name='empresas',
        verbose_name='Sector'
    )
    nit = models.CharField(
        max_length=20,
        unique=True,
        blank=True,
        null=True,
        verbose_name='NIT'
    )
    direccion = models.TextField(blank=True, null=True, verbose_name='Dirección')
    telefono = models.CharField(max_length=20, blank=True, null=True, verbose_name='Teléfono')
    email = models.EmailField(blank=True, null=True, verbose_name='Email')
    
    class Meta:
        db_table = 'empresa'
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre
