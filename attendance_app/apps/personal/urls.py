from django.urls import path


from attendance_app.apps.personal.views import facultades, tipo_personal, personal, personal_por_tipo, personal_con_asistencias

urlpatterns = [
    path('facultades', facultades),
    path('tipo-personal', tipo_personal),
    path('personal-por-tipo/<int:id_tipo>', personal_por_tipo),
    path('personal-con-asistencias', personal_con_asistencias),
    # path('validar-imagen', validar_imagen),
    path('', personal)
]
