from appDb.models import VacacionLicencia
from appDb.models import Usuario
from appDb.models import Trabajador
from django.shortcuts import render, redirect
from django.views.generic import ListView
from appDb.views import login_view
from django.contrib.auth.mixins import LoginRequiredMixin
from appRRHH.forms import *
def solicitud_licencia(request):
    if request.method == 'POST':
        # Obtener los datos enviados por el formulario de solicitud de licencia
        tipo_solicitud = request.POST.get('tipo_solicitud')
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')
        dias = request.POST.get('dias')

        # Obtener el usuario del trabajador de la sesión
        usuario = Usuario.objects.get(nombre_usuario=request.session['nombre_usuario'])

        # Obtener el trabajador relacionado con el usuario
        trabajador = Trabajador.objects.get(id_usuario=usuario)

        # Crear una nueva instancia de VacacionLicencia
        vacacion_licencia = VacacionLicencia(
            rut=trabajador,
            tipo_solicitud=tipo_solicitud,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            dias=dias,
            estado='Pendiente'
        )

        # Guardar la solicitud de licencia en la base de datos
        vacacion_licencia.save()

        # Redirigir a una página de éxito o mostrar un mensaje de éxito
        return redirect('listaLicencias')

    return render(request, 'trabajador/solicitud_licencia_form.html')

def modulo_Trabajador(request):
    return render(request, 'trabajador/moduloTrabajador.html')


def misSolicitudes(request):
    if request.method == 'GET':
        # Obtener el usuario del trabajador de la sesión
        usuario = Usuario.objects.get(nombre_usuario=request.session['nombre_usuario'])

        # Obtener el trabajador relacionado con el usuario
        trabajador = Trabajador.objects.get(id_usuario=usuario)

        # Obtener las solicitudes enviadas por el trabajador
        solicitudes = VacacionLicencia.objects.filter(rut=trabajador)

        # Pasar las solicitudes al contexto del template para visualizarlas
    return render(request, 'trabajador/solicitud_licencia_success.html', {'solicitudes': solicitudes})