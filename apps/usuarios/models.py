from django.db import models


class Usuario(models.Model):
    """
    Representa a un usuario del sistema.
    """
    id_usuario = models.AutoField(primary_key=True)
    nom_usuario = models.CharField(max_length=100)
    clave = models.CharField(max_length=100)

    class Meta:
        managed = False 
        db_table = 'usuario'

    def __str__(self):
        return self.nom_usuario


class OpcionCrud(models.Model):
    """
    Define las opciones o módulos disponibles en el sistema.
    """
    id_opcion = models.IntegerField(primary_key=True)
    des_opcion = models.CharField(max_length=100, blank=True, null=True)
    num_form = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'opcion_crud'

    def __str__(self):
        return self.des_opcion or f"Opción {self.id_opcion}"


class AccesoUsuario(models.Model):
    """
    Relaciona usuarios con las opciones a las que tienen acceso.
    Puede incluir una empresa específica si aplica.
    """
    id_usuario = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='id_usuario')
    id_opcion = models.ForeignKey(OpcionCrud, models.DO_NOTHING, db_column='id_opcion')
    empresa_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'acceso_usuario'
        unique_together = (('id_usuario', 'id_opcion'),)

    def __str__(self):
        return f"{self.id_usuario} → {self.id_opcion}"