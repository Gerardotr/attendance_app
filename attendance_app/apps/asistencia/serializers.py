from rest_framework import serializers

from attendance_app.apps.asistencia.models import Asistencia
from attendance_app.apps.personal.serializers import GetPersonalSerialiser


class SetAsistenciaSerializer(serializers.ModelSerializer):
   class Meta:
       model = Asistencia
       fields = ['id', 'personal', 'imagen', 'evento', 'tipo_evento']


class GetAsistenciaSerializer(serializers.ModelSerializer):

   personal = GetPersonalSerialiser()

   class Meta:
       model = Asistencia
       fields = ['id', 'personal', 'creado', 'imagen','evento', 'tipo_evento']

