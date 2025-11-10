from django.db import models


class ModeloBase(models.Model):
    """
    Modelo base abstracto para todos los modelos del sistema.
    Proporciona campos comunes de auditoría y control.
    """
    creado_en = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    actualizado_en = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')
    
    class Meta:
        abstract = True
        ordering = ['-creado_en']

