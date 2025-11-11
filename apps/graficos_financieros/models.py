from django.db import models
from django.contrib.auth.models import User
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


class ProyeccionVenta(ModeloBase):
    """
    Tabla de proyecciones de ventas generadas por otros módulos.
    Esta tabla YA EXISTE en la BD, solo la registramos en Django.
    """
    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.CASCADE,
        related_name='proyecciones_ventas',
        verbose_name='Empresa'
    )
    año = models.IntegerField(
        db_column='anio',  # La columna en BD se llama 'anio' sin ñ
        verbose_name='Año',
        help_text='Año de la proyección'
    )
    mes = models.IntegerField(
        verbose_name='Mes',
        help_text='Mes (1-12)'
    )
    metodo = models.CharField(
        max_length=100,
        verbose_name='Método de proyección',
        help_text='Incremento Porcentual, Incremento Absoluto, Mínimos Cuadrados'
    )
    valor_proyectado = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        verbose_name='Valor proyectado',
        help_text='Valor de venta proyectado'
    )
    
    class Meta:
        db_table = 'proyeccion_ventas'
        managed = False  # Django no gestiona esta tabla (ya existe)
        verbose_name = 'Proyección de Venta'
        verbose_name_plural = 'Proyecciones de Ventas'
        ordering = ['año', 'mes']
    
    def __str__(self):
        return f'{self.empresa.nombre} - {self.año}/{self.mes:02d} - {self.metodo}'


class RatioFinanciero(ModeloBase):
    """
    Catálogo de ratios financieros disponibles.
    Tabla: ratio_financiero
    """
    nombre = models.CharField(
        max_length=200,
        verbose_name='Nombre del Ratio',
        help_text='Ejemplo: Razón Corriente, Prueba Ácida'
    )
    formula_display = models.CharField(
        max_length=500,
        verbose_name='Fórmula',
        help_text='Ejemplo: Activo Corriente / Pasivo Corriente'
    )
    categoria = models.CharField(
        max_length=100,
        verbose_name='Categoría',
        help_text='Ejemplo: Liquidez, Endeudamiento, Rentabilidad'
    )
    promedio_general = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        null=True,
        blank=True,
        verbose_name='Promedio General'
    )
    
    class Meta:
        db_table = 'ratio_financiero'
        verbose_name = 'Ratio Financiero'
        verbose_name_plural = 'Ratios Financieros'
        ordering = ['categoria', 'nombre']
    
    def __str__(self):
        return f'{self.nombre} ({self.categoria})'


class ValorRatioCalculado(ModeloBase):
    """
    Valores calculados de ratios financieros por año y empresa.
    Tabla: valor_ratio_calculado
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
        related_name='valores',
        verbose_name='Ratio'
    )
    usuario_calculo = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Usuario que calculó'
    )
    
    año = models.IntegerField(
        verbose_name='Año',
        help_text='Año del cálculo (Ej: 2022, 2023, 2024)'
    )
    valor_calculado = models.DecimalField(
        max_digits=15,
        decimal_places=4,
        verbose_name='Valor Calculado'
    )
    
    # Campos de comparación
    parametro_sectorial = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        null=True,
        blank=True,
        verbose_name='Parámetro Sectorial'
    )
    promedio_sector = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        null=True,
        blank=True,
        verbose_name='Promedio del Sector'
    )
    promedio_general = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        null=True,
        blank=True,
        verbose_name='Promedio General'
    )
    
    # Flags de superación
    superior_parametro_sectorial = models.BooleanField(
        default=False,
        verbose_name='Supera Parámetro Sectorial'
    )
    superior_promedio_sector = models.BooleanField(
        default=False,
        verbose_name='Supera Promedio del Sector'
    )
    superior_promedio_general = models.BooleanField(
        default=False,
        verbose_name='Supera Promedio General'
    )
    
    fecha_calculo = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Cálculo'
    )
    
    class Meta:
        db_table = 'valor_ratio_calculado'
        verbose_name = 'Valor de Ratio Calculado'
        verbose_name_plural = 'Valores de Ratios Calculados'
        ordering = ['empresa', 'ratio', '-año']
        unique_together = [['empresa', 'ratio', 'año']]
    
    def __str__(self):
        return f'{self.empresa.nombre} - {self.ratio.nombre} ({self.año}): {self.valor_calculado}'


class AnalisisRatio(ModeloBase):
    """
    Modelo para guardar análisis de ratios generados.
    Similar a ProyeccionFinanciera pero para ratios.
    """
    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.CASCADE,
        related_name='analisis_ratios',
        verbose_name='Empresa'
    )
    nombre = models.CharField(
        max_length=200,
        verbose_name='Nombre del Análisis',
        help_text='Ejemplo: Análisis de Ratios 2022-2024'
    )
    descripcion = models.TextField(
        blank=True,
        verbose_name='Descripción'
    )
    
    # Datos del gráfico en JSON
    # Estructura: {
    #   'ratios': ['Razón Corriente', 'Prueba Ácida', ...],
    #   'años': [2022, 2023, 2024],
    #   'datos': {
    #     'Razón Corriente': [0.26, 0.25, 0.25],
    #     'Prueba Ácida': [0.24, 0.23, 0.23],
    #     ...
    #   }
    # }
    datos_grafico = models.JSONField(
        null=True,
        blank=True,
        verbose_name='Datos del Gráfico'
    )
    
    class Meta:
        db_table = 'analisis_ratio'
        verbose_name = 'Análisis de Ratios'
        verbose_name_plural = 'Análisis de Ratios'
        ordering = ['-creado_en']
    
    def __str__(self):
        return f'{self.empresa.nombre} - {self.nombre}'

