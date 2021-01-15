from django.urls import path


from attendance_app.apps.asistencia.views import asistencia, asistencia_por_personal, asistencia_por_personal_rango
urlpatterns = [

    path('', asistencia),
    path('asistencia-personal/<int:id_personal>', asistencia_por_personal),
    path('asistencia-personal-rango/<int:id_personal>', asistencia_por_personal_rango),

]
