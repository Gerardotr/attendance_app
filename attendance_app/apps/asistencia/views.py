import cloudinary
import cloudinary.uploader
import cloudinary.api
import uuid

from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from attendance_app.apps.asistencia.models import Asistencia, Personal
from attendance_app.apps.asistencia.serializers import SetAsistenciaSerializer, GetAsistenciaSerializer

from datetime import date, datetime, timedelta
from django.utils import timezone
import datetime as dt
import time
from PIL import Image
import numpy as np
import face_recognition
import cv2


@api_view(['GET', 'POST'])
def asistencia(request):
    if request.method == "GET":
        fecha = request.GET.get('fecha', '')

        fecha = datetime.today() if fecha == '' else datetime.strptime(fecha, '%d-%m-%Y')

        id_persona = int(request.GET.get('idPersona', '0'))

        if id_persona != 0:
            listado = Asistencia.objects.filter(creado__date=fecha.date(), personal_id=id_persona)
        else:
            listado = Asistencia.objects.filter(creado__date=fecha.date())

        serializer = GetAsistenciaSerializer(listado, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        mensaje = False
        id_personal = int(request.GET.get('persona'))
        evento = 0

        file_in_memory = request.FILES['imagen']

        try:
            asistencias_persona = Asistencia.objects.filter(personal_id=id_personal, creado__date=date.today()).last()

            diferencia = abs(datetime.now() - asistencias_persona.creado)
            minutos = divmod(diferencia.seconds, 60)

            if minutos[0] > 10:

                if asistencias_persona.evento == 0:
                    evento = 1
                mensaje = registrar_asistencia(id_personal, file_in_memory, evento)

        except:
            mensaje = registrar_asistencia(id_personal, file_in_memory, evento=evento)

        return Response({'mensaje': mensaje})


def guardar_imagen(file_in_memory):
    content_type = file_in_memory.content_type
    filename = str(uuid.uuid4()) + '.jpg'
    archivo = SimpleUploadedFile(filename, file_in_memory.read(), content_type)
    res = cloudinary.uploader.upload(archivo)
    return res['secure_url']


@api_view(['GET'])
def asistencia_por_personal(request, id_personal):
    listado = Asistencia.objects.filter(personal_id=id_personal)
    asistencia_personal_serializer = GetAsistenciaSerializer(listado, many=True)

    return Response(asistencia_personal_serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def asistencia_por_personal_rango(request, id_personal):
    fecha1 = request.GET.get('fecha1', '')
    fecha2 = request.GET.get('fecha2', '')

    fecha1 = datetime.strptime(fecha1, '%d-%m-%y')
    fecha2 = datetime.strptime(fecha2, '%d-%m-%y') + timedelta(days=1)

    listado = Asistencia.objects.filter(personal_id=id_personal, creado__rabge=[fecha1, fecha2])
    asistencia_personal_serializer = GetAsistenciaSerializer(listado, many=True)

    return Response(asistencia_personal_serializer.data, status=status.HTTP_200_OK)


def registrar_asistencia(id, image_file, evento):
    image_url = guardar_imagen(image_file)

    asistencia_data = {'personal': id, 'imagen': image_url, 'evento': evento, 'tipo_evento': tipo_evento()}

    asistencia_serializer = SetAsistenciaSerializer(data=asistencia_data)

    if asistencia_serializer.is_valid():
        asistencia_serializer.save()
        return True
    else:

        return asistencia_serializer.errors


def tipo_evento():
    hora = datetime.now().hour
    if hora < 12:
        return 0
    else:
        return 1
