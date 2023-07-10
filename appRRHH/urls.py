from django.urls import path
from appRRHH import views
from appRRHH.views import ListadoTrabajador
from appRRHH.views import GestionSolicitud


urlpatterns = [
    path('visualizar/', ListadoTrabajador.as_view(), name='visualizar'),
    path('',views.moduloJefeRRHH,name='modulo_jefeRRHH'),
    path('moduloRRHH/',views.moduloRRHH,name='modulo_RRHH'),
    path('moduloTrabajador/',views.moduloTrabajador,name='modulo_trabajador'),
    path('prueba/',views.prueba,name='prueba'),
    path('ficha/trabajador/',views.fichaTrabajador,name='fichaTrabajador'),
    path('ficha/area/',views.fichaArea,name='fichaArea'),
    path('ficha/departamento/', views.fichaDepartamento, name='fichaDepartamento'),
    path('ficha/cargo/', views.fichaCargo, name='fichaCargo'),
    path('Gestion/solicitud/', GestionSolicitud.as_view(), name='solicitudes'),

]




