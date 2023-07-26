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

def consulta_personalizada(request):
    # Obtenemos el 'nombre_perfil' del usuario desde la sesión
    nombre_perfil = request.session.get('nombre_perfil', None)

    # Inicializamos 'result' como un diccionario vacío
    result = {}

    # Verificamos si el usuario ha iniciado sesión y si su 'nombre_perfil' es 'Trabajador'
    if nombre_perfil == 'Trabajador':
        # Obtenemos el 'rut' del trabajador desde la sesión
        rut_trabajador = request.session.get('rut_trabajador', None)
        if rut_trabajador:
            # Realizamos la consulta personalizada utilizando el 'rut_trabajador'
            trabajador = Trabajador.objects.filter(rut=rut_trabajador).first()
            if trabajador:
                result['trabajador'] = trabajador
                result['cargas_familiares'] = trabajador.cargafamiliar_set.all()
                result['contactos_emergencia'] = trabajador.contactoemergencia_set.all()

    # Pasamos los resultados a la plantilla para mostrarlos
    return render(request, 'trabajador/consulta_personalizada.html', {'result': result})

def editar_informacion_personal(request, rut_trabajador):
    try:
        trabajador = Trabajador.objects.get(rut=rut_trabajador)
    except Trabajador.DoesNotExist:
        # Manejo del caso donde el trabajador no existe
        return redirect('ruta_de_vista_de_error')  # Cambia 'ruta_de_vista_de_error' por la vista de manejo de error que desees

    if request.method == 'POST':
        # Si se envió el formulario con los datos editados
        trabajador.nombre = request.POST.get('nombre', trabajador.nombre)
        trabajador.sexo = request.POST.get('sexo', trabajador.sexo)
        trabajador.direccion = request.POST.get('direccion', trabajador.direccion)
        trabajador.telefono = request.POST.get('telefono', trabajador.telefono)

        # Cargas Familiares
        num_cargas = int(request.POST.get('num_cargas', 0))
        trabajador.cargafamiliar_set.all().delete()  # Eliminamos las cargas familiares anteriores
        for i in range(num_cargas):
            cf_nombre = request.POST.get(f'cf_nombre_{i}', '')
            cf_parentesco = request.POST.get(f'cf_parentesco_{i}', '')
            cf_sexo = request.POST.get(f'cf_sexo_{i}', '')
            trabajador.cargafamiliar_set.create(cf_nombre=cf_nombre, parentesco=cf_parentesco, cf_sexo=cf_sexo)

        # Contactos de Emergencia
        num_contactos = int(request.POST.get('num_contactos', 0))
        trabajador.contactoemergencia_set.all().delete()  # Eliminamos los contactos de emergencia anteriores
        for i in range(num_contactos):
            ce_nombre = request.POST.get(f'ce_nombre_{i}', '')
            ce_relacion = request.POST.get(f'ce_relacion_{i}', '')
            ce_telefono = request.POST.get(f'ce_telefono_{i}', '')
            trabajador.contactoemergencia_set.create(ce_nombre=ce_nombre, relacion_con_trabajador=ce_relacion,
                                                     ce_telefono=ce_telefono)

        trabajador.save()
        return redirect('consulta_personalizada')  # Cambia 'ruta_de_vista_de_consulta_personalizada' por la vista de consulta personalizada que creaste

    return render(request, 'trabajador/editar_informacion_personal.html', {'trabajador': trabajador})