from django.urls import path,include
from appRRHH import views
from appRRHH.views import listadotrabajador
from appRRHH.views import GestionSolicitud
from appRRHH.views import Ver_liquidacion
from appRRHH.views import Ver_registro_medico
from appRRHH.views import ListSolicitudes



urlpatterns = [
    path('listTrabajadores/',listadotrabajador.as_view(), name='listTrabajadores'),
    path('listSolicitudes/',ListSolicitudes.as_view(), name='listSolicitudes'),
    path('',views.moduloJefeRRHH,name='modulo_jefeRRHH'),
    path('moduloRRHH/',views.moduloRRHH,name='modulo_RRHH'),
    path('moduloTrabajador/',views.moduloTrabajador,name='modulo_trabajador'),
    path('ficha/trabajador/',views.fichaTrabajador,name='fichaTrabajador'),
    path('ficha/area/',views.fichaArea,name='fichaArea'),
    path('ficha/departamento/',views.fichaDepartamento, name='fichaDepartamento'),
    path('ficha/cargo/',views.fichaCargo, name='fichaCargo'),
    path('Gestion/solicitud/',GestionSolicitud.as_view(), name='solicitudes'),
    path('crear_liquidacion/',views.crear_liquidacion,name='crear_liquidacion'),
    path('ver_ficha_liquidaciones/',Ver_liquidacion.as_view(),name='ver_ficha_liquidaciones'),
    path('crear_registro_medico/',views.crear_registro_medico,name='crear_registro_medico'),
    path('ver_registro_medico/',Ver_registro_medico.as_view(),name='ver_registro_medico'),


]




