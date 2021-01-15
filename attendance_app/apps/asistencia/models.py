from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone

from attendance_app.apps.personal.models import Personal


# Create your models here.
class Asistencia(models.Model):
   personal = models.ForeignKey(Personal, on_delete=models.PROTECT, related_name='personal_id')
   imagen = models.TextField(blank=False, null=False)
   creado = models.DateTimeField(default=timezone.now)
   evento = models.SmallIntegerField(blank=True, null=True)
   tipo_evento = models.SmallIntegerField(blank=True, null=True)



   class Meta:
       db_table = 'asistencia'

