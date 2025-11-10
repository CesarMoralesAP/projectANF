from django.db import models
from apps.core.models import ModeloBase
from apps.empresas.models import Empresa


class OrigenDatos(models.TextChoices):
    """
    Origen de los datos de la proyección.
    """
    CALCULADO = 'CALCULADO', 'Calculado en la aplicación'
    ARCHIVO = 'ARCHIVO', 'Subido desde archivo Excel'


class ProyeccionFinanciera(ModeloBase):
    """
    Modelo para almacenar proyecciones financieras.
    Soporta datos de archivo Excel o cálculos internos (híbrido).
    """
    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.CASCADE,
        related_name='proyecciones',
        verbose_name='Empresa'
    )
    nombre = models.CharField(
        max_length=200,
        verbose_name='Nombre de la proyección',
        help_text='Ejemplo: Proyección 2025 - Banco Agrícola'
    )
    descripcion = models.TextField(
        blank=True,
        verbose_name='Descripción',
        help_text='Descripción opcional de la proyección'
    )
    
    # Origen de los datos
    origen = models.CharField(
        max_length=20,
        choices=OrigenDatos.choices,
        default=OrigenDatos.ARCHIVO,
        verbose_name='Origen de datos'
    )
    
    # Archivo Excel (solo si origen = ARCHIVO)
    archivo = models.FileField(
        upload_to='proyecciones/%Y/%m/',
        null=True,
        blank=True,
        verbose_name='Archivo Excel',
        help_text='Archivo Excel con datos de proyección'
    )
    
    # Datos procesados en formato JSON
    # Estructura: {
    #   'valor_incremental': {'periodos': [...], 'valores': [...]},
    #   'valor_absoluto': {'periodos': [...], 'valores': [...]}
    # }
    datos_grafico = models.JSONField(
        null=True,
        blank=True,
        verbose_name='Datos del gráfico',
        help_text='Datos procesados para visualización'
    )
    
    class Meta:
        db_table = 'proyeccion_financiera'
        verbose_name = 'Proyección Financiera'
        verbose_name_plural = 'Proyecciones Financieras'
        ordering = ['-creado_en']
    
    def __str__(self):
        return f'{self.empresa.nombre} - {self.nombre}'

