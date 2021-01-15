import uuid

import cloudinary
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from attendance_app.apps.asistencia.models import Asistencia
from attendance_app.apps.personal.models import Facultad, TipoPersonal, Personal
from attendance_app.apps.personal.serializers import FacultadSerializer, TipoPersonalSerializer, GetPersonalSerialiser, \
    SetPersonalSerialiser

from PIL import Image
import numpy as np
import face_recognition
import cv2
from datetime import date


@api_view(['GET', 'POST'])
def facultades(request):
    estado = status.HTTP_500_INTERNAL_SERVER_ERROR
    if request.method == "GET":
        listado = Facultad.objects.all()
        serializer = FacultadSerializer(listado, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        datos = request.data
        for data in datos:
            serializer = FacultadSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                estado = status.HTTP_200_OK

        return Response(status=estado)


@api_view(['GET'])
def personal_por_facultad(request, id_facultad):
    listado = Personal.objects.filter(facultad_id=id_facultad)
    personal_serializer = GetPersonalSerialiser(listado, many=True)

    return Response(personal_serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def personal_por_tipo(request, id_tipo):
    listado = Personal.objects.filter(tipo_personal_id=id_tipo)
    personal_serializer = GetPersonalSerialiser(listado, many=True)

    return Response(personal_serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def tipo_personal(request):
    estado = status.HTTP_500_INTERNAL_SERVER_ERROR

    if request.method == "GET":
        listado = TipoPersonal.objects.all()
        serializer = TipoPersonalSerializer(listado, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        datos = request.data
        for data in datos:
            serializer = TipoPersonalSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                estado = status.HTTP_200_OK

        return Response(status=estado)


@api_view(['GET', 'POST'])
def personal(request):
    if request.method == "GET":
        listado = Personal.objects.all()
        serializer = GetPersonalSerialiser(listado, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':

        mensaje = {'mensaje': 'La imagen no es valida'}

        try:

            file_in_memory = request.FILES['imagen']

            persona = request.data

            foto = guardar_imagen(file_in_memory)

            encoded_image = image_file_to_numpy_array(file_in_memory)

            if encoded_image is None:

                return Response(mensaje, status=status.HTTP_400_BAD_REQUEST)

            else:

                persona['foto'] = foto

                persona['encoded_image'] = encoded_image

                serializer = SetPersonalSerialiser(data=persona)

                if serializer.is_valid():

                    serializer.save()

                    return Response(serializer.data, status=status.HTTP_201_CREATED)

                else:

                    print(serializer.errors)

                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:

            print(e)

            return Response(status=status.HTTP_400_BAD_REQUEST)


def guardar_imagen(file_in_memory):
    content_type = file_in_memory.content_type
    filename = str(uuid.uuid4()) + '.jpg'
    archivo = SimpleUploadedFile(filename, file_in_memory.read(), content_type)
    res = cloudinary.uploader.upload(archivo)
    return res['secure_url']


@api_view(['GET'])
def personal_con_asistencias(request):
    if request.method == "GET":
        listado = Personal.objects.all()
        listado_filtrado = filter(
            lambda x: Asistencia.objects.filter(personal_id=x.id, creado__date=date.today()).last() is not None,
            listado)
        serializer = GetPersonalSerialiser(list(listado_filtrado), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


def image_file_to_numpy_array(file_in_memory):
    stream = file_in_memory.file
    img = Image.open(stream).convert("RGBA")
    cur_img = np.array(img)
    img1 = cv2.cvtColor(cur_img, cv2.COLOR_BGR2RGB)
    str_array = None
    try:
        encode = face_recognition.face_encodings(img1)[0]
        str_array = np.array_str(encode)
    except:
        pass
    return str_array

# @api_view(['POST'])
# def validar_imagen(request):
#
#     file_in_memory = request.FILES['encoded_image']
#     data = image_file_to_numpy_array(file_in_memory)
#
#     if data is not None:
#         return Response(data, status=status.HTTP_200_OK)
#
#     else:
#         return Response(data, status=status.HTTP_400_BAD_REQUEST)
