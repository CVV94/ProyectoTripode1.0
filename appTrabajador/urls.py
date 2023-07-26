from django.urls import path
from appTrabajador import views
# from appTrabajador.views import ListSolicitudes


# from django.views.generic import TemplateView

urlpatterns = [
    path('solicitud-licencia/',views.solicitud_licencia, name='solicitud_licencia'),
    path('modulo/trabajador/',views.modulo_Trabajador, name='modulo_trabajador'),
    path('listado/licencias/',views.misSolicitudes, name='listaLicencias'),
    path('consulta/', views.consulta_personalizada, name='consulta_personalizada'),
    path('editar-informacion/<str:rut_trabajador>/',views.editar_informacion_personal, name='editar_informacion_personal'),
    path('agregar_carga_familiar/', views.agregar_carga_familiar, name='agregar_carga_familiar'),
    path('agregar_contacto_emergencia/', views.agregar_contacto_emergencia, name='agregar_contacto_emergencia'),
]
