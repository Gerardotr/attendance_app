from django.db import models
from django.utils import timezone

# Create your models here.

class TipoPersonal(models.Model):
    nombre = models.CharField(max_length=256, null=False, blank=False)
    alias = models.CharField(max_length=3, null=False, blank=False)
    creado = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'tipo_personal'


class Facultad(models.Model):
    nombre = models.CharField(max_length=255, null=False, blank=False)
    alias = models.CharField(max_length=3, null=False, blank=False)
    creado = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'facultad'

class Personal(models.Model):
    nombre = models.CharField(max_length=255, null=False, blank=False)
    apellidos = models.CharField(max_length=255, null=False, blank=False)
    codigo = models.CharField(max_length=255, null=True, blank=False)
    correo = models.EmailField(max_length=255, null=False, blank=False)
    encoded_image = models.TextField(null=False, blank=False)
    foto = models.TextField(null=True, blank=True)
    facultad = models.ForeignKey(Facultad, on_delete=models.PROTECT, related_name='facultad')
    tipo_personal = models.ForeignKey(TipoPersonal, on_delete=models.PROTECT, related_name='tipo_personal')
    creado = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'personal'

