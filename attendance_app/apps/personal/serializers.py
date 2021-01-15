from rest_framework import serializers

from attendance_app.apps.personal.models import Facultad, TipoPersonal , Personal


class FacultadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Facultad
        fields = ['id', 'nombre', 'alias', 'creado']


class TipoPersonalSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoPersonal
        fields = ['id', 'nombre', 'alias', 'creado']


class GetPersonalSerialiser(serializers.ModelSerializer):
   facultad = FacultadSerializer()
   tipo_personal = TipoPersonalSerializer()

   class Meta:
       model = Personal
       fields = ['id', 'nombre', 'apellidos', 'codigo', 'correo', 'encoded_image', 'foto', 'facultad', 'tipo_personal', 'creado']


class SetPersonalSerialiser(serializers.ModelSerializer):
   class Meta:
       model = Personal
       fields = ['id', 'nombre', 'apellidos', 'codigo', 'correo', 'encoded_image', 'foto', 'facultad', 'tipo_personal', 'creado']

