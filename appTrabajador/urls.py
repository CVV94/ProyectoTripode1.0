from django.urls import path
from django.contrib.auth import views as auth_views
from appTrabajador import views



# from django.views.generic import TemplateView

urlpatterns = [
    path('solicitud-licencia/',views.solicitud_licencia, name='solicitud_licencia'),
]
