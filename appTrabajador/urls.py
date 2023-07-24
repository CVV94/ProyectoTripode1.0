from django.urls import path
from appTrabajador import views
# from appTrabajador.views import ListSolicitudes


# from django.views.generic import TemplateView

urlpatterns = [
    path('solicitud-licencia/',views.solicitud_licencia, name='solicitud_licencia'),
    path('modulo/trabajador/',views.modulo_Trabajador, name='modulo_trabajador'),
    path('listado/licencias/',views.misSolicitudes, name='listaLicencias'),
]
