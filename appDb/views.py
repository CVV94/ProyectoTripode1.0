from typing import Any, Dict
from django.db.models.query import QuerySet
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from .models import Usuario
from .models import Trabajador
from .models import Perfil
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required   



def hola(request):
    return render(request,'base/hola.html')

def registrarse(request):
    if request.method == 'POST':
        nombre_usuario = request.POST['nombre_usuario']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        perfil_id = request.POST['perfil']

        # Verificar si la contraseña y la confirmación coinciden
        if password != confirm_password:
            messages.error(request, 'Las contraseñas no coinciden')
            return render(request,'base/crear_usuario.html')  # Redireccionar a la página de registro nuevamente

        try:
            # Verificar si el nombre de usuario ya existe en la base de datos
            Usuario.objects.get(nombre_usuario=nombre_usuario)
            messages.error(request, 'El nombre de usuario ya está en uso')
            return redirect('registro')  # Redireccionar a la página de registro nuevamente

        except Usuario.DoesNotExist:
            try:     
                # Obtener el perfil seleccionado por su ID
                perfil = Perfil.objects.get(id_perfil=perfil_id)

                # Crear un nuevo objeto Usuario en la base de datos y asignar el perfil
                usuario = Usuario(nombre_usuario=nombre_usuario, password=password, id_perfil=perfil)
                usuario.save()

                messages.success(request, '¡Registro exitoso! Ahora puedes iniciar sesión')
                return redirect('login')  # Redireccionar a la página de inicio de sesión

            except Perfil.DoesNotExist:
                messages.error(request, 'El perfil seleccionado no existe')
                return redirect('registro')  # Redireccionar a la página de registro nuevamente

    # Obtener todos los perfiles existentes
    perfiles = Perfil.objects.all()

    if perfiles:
        # Renderizar el formulario de registro con los perfiles disponibles
        return render(request, 'base/crear_usuario.html', {'perfiles': perfiles})
    else:
        messages.error(request, 'No existen perfiles disponibles')
        return redirect('registro')  # Redireccionar a la página de registro nuevamente



def index(request):
    return render(request, 'base/index.html')    


def crear_perfil(request):
    if request.method == 'POST':
        nombre_perfil=request.POST.get('nombre_perfil')
        try:
            crearPerfiles= Perfil(nombre_perfil=nombre_perfil)
            crearPerfiles.save()
            return redirect('perfil')
        except Exception as e:
            messages.error(request,'Ocurrio un error al crear el Perfil:{}'.format(str(e)))
    return render(request,'base/crear_perfil.html')


def login_view(request):
    if request.method == 'POST':
        nombre_usuario = request.POST['nombre_usuario']
        password = request.POST['password']
        
        try:
            detalleUsuario = Usuario.objects.get(nombre_usuario=nombre_usuario, password=password)
            detalleTrabajador = Trabajador.objects.get(id_usuario=detalleUsuario)
            request.session['nombre_usuario'] = detalleUsuario.nombre_usuario
            request.session['nombre_perfil'] = detalleUsuario.id_perfil.nombre_perfil
            request.session['rut_trabajador'] = detalleTrabajador.rut  # Guardar el rut del trabajador

            if request.session['nombre_perfil'] == 'Trabajador':
                return redirect('solicitud_licencia')

            return render(request, 'base/hola.html')

        except Usuario.DoesNotExist:
            messages.error(request, 'El nombre de usuario o la contraseña no son correctos.')
    
    return render(request, 'base/login.html')


def logout_view(request):
    if 'nombre_usuario' in request.session:
        del request.session['nombre_usuario'] # Del es ugual a delete pero significa si existe un nombre Usuario autentificado
        messages.success(request, 'Has cerrado sesión exitosamente.')
    else:
        messages.error(request, 'No has iniciado sesión.')
    
    return redirect('login')