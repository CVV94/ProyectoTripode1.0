from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy   # importacion para redireccionamientos de django con clases
from django.views.generic import CreateView
from appRRHH.forms import LicenciaForm
from appDb.models import Trabajador
from appDb.models import Cargo
from appDb.models import Usuario
from appDb.models import Departamento
from appDb.models import Area
from appDb.models import VacacionLicencia
from appDb.models import Liquidacion
from appDb.models import RegistroMedico

def moduloRRHH(request):
    return render(request, 'RRHH/moduloRRHH.html')  # redireccionar a la página del módulo de rrhh.


def moduloJefeRRHH(request):
    return render(request,'RRHH/moduloJefeRRHH.html') # redireccionar a la página del módulo de jefe de rrhh.


def moduloTrabajador(request):
    return render(request,'RRHH/moduloRRHH.html') # redireccionar a la página del módulo de trabajador


login_required
class listadotrabajador(ListView):
    model = Trabajador                                  #modelo con el que trabaja
    template_name = 'RRHH/trabajadores.html'         #direccion template

    def get_queryset(self):                             #consultas de orm
        trabajadores = Trabajador.objects.select_related('id_cargo').values('rut', 'nombre', 'sexo', 'id_cargo__nombre_cargo')
        return trabajadores

    def get_context_data(self, **kwargs):             #pasa un contexto de las consultas a la planilla html{{}}
        context = super().get_context_data(**kwargs)
        context['title'] = 'listado de trabajadores'
        context['trabajadores'] = self.get_queryset()
        return context

class ListSolicitudes(ListView):
    model = VacacionLicencia
    template_name = 'RRHH/list_solicitudes.html'
    def dispatch(self, request, *args, **kwargs):           # Se usa para redireccionar
        return super().dispatch(request, *args, **kwargs)
    def get_queryset(self):
        solicitudes = VacacionLicencia.objects.all()
        return solicitudes
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'listado de Solicitudes'
        context["solicitudes"] = self.get_queryset()
        return context
    
class GestionSolicitud(CreateView):
    model = VacacionLicencia
    form_class= LicenciaForm
    template_name = 'RRHH/gestionsolicitud.html'
    success_url = reverse_lazy('listSolicitudes')

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['title'] = 'gestion de solicitudes'
        return context
    


def fichaTrabajador(request):
    if request.method == 'post':
        rut = request.post.get('rut')
        nombre = request.post.get('nombre')
        sexo = request.post.get('sexo')
        direccion = request.post.get('direccion')
        telefono = request.post.get('telefono')
        fecha_ingreso = request.post.get('fecha_ingreso')
        id_cargo = request.post.get('id_cargo')
        id_usuario = request.post.get('id_usuario')

        try:
            cargo = Cargo.objects.get(id_cargo=id_cargo)
            usuario = Usuario.objects.get(id_usuario=id_usuario)
            trabajador = Trabajador(rut=rut, nombre=nombre, sexo=sexo, direccion=direccion, telefono=telefono, fecha_ingreso=fecha_ingreso, id_cargo=cargo, id_usuario=usuario)
            trabajador.save()
            return redirect('fichatrabajador')  # redireccionar a la misma página después de guardar
        except Exception as e:
            messages.error(request, 'ocurrió un error al crear la ficha del trabajador: {}'.format(str(e)))
            return redirect('fichatrabajador')  # redireccionar a la misma página si ocurre una excepción

    cargos = Cargo.objects.all()
    usuarios = Usuario.objects.all()

    if cargos.exists() and usuarios.exists():  # usar 'and' en lugar de 'or'
        return render(request, 'rrhh/fichatrabajador.html', {'cargos': cargos, 'usuarios': usuarios})
    else:
        messages.error(request, 'no existen cargos y usuarios disponibles')
        return redirect('fichatrabajador')

def fichaArea(request):
    if request.method == 'post':
        id_area = request.post.get('id_area')
        nombre_area = request.post.get('nombre_area')
        try:
            area = Area(id_area=id_area, nombre_area=nombre_area)
            area.save()
            return redirect('fichadepartamento') # redireccionar con el argumento id_area
        except Exception as e:
            messages.error(request, 'ocurrió un error al crear el área: {}'.format(str(e)))
            return render(request, 'rrhh/fichaarea.html')
    return render(request, 'RRHH/fichaarea.html')

def fichaDepartamento(request):
    if request.method == 'post':
        id_departamento = request.post.get('id_departamento')
        id_area = request.post.get('id_area')  # corregir el nombre del campo a 'id_area'
        departamento = request.post.get('departamento')
        try:
            area = Area.objects.get(id_area=id_area)
            departamento = Departamento(id_departamento=id_departamento, id_area=area, departamento=departamento)  # usar 'id_area' en lugar de 'area'
            departamento.save()
            messages.success(request, 'departamento creado exitosamente.')
            return redirect('fichacargo')
        except Exception as e:
            messages.error(request, 'ocurrió un error al crear el departamento: {}'.format(str(e)))
            return render(request, 'RRHH/fichadepartamento.html')

    areas = Area.objects.all()
    if areas:
        return render(request, 'RRHH/fichadepartamento.html', {'areas': areas})
    else:
        messages.error(request, 'no existen áreas disponibles')
        return redirect('fichadepartamento')

def fichaCargo(request):
    if request.method == 'post':
        id_cargo=request.post.get('id_cargo')
        id_departamento=request.post.get('id_departamento')
        nombre_cargo=request.post.get('nombre_cargo')
        try:
            departamento=Departamento.objects.get(id_departamento=id_departamento)
            cargo=Cargo(id_cargo=id_cargo,id_departamento=departamento,nombre_cargo=nombre_cargo)
            cargo.save()
            messages.success(request, 'cargo creado exitosamente.')
            return redirect('fichatrabajador')
        except Exception as e:
            messages.error(request, 'ocurrió un error al crear el cargo: {}'.format(str(e)))
            return render(request, 'RRHH/fichaCargo.html')
    departamentos = Departamento.objects.all()

    if departamentos:
        return render(request, 'RRHH/fichaCargo.html', {'departamentos': departamentos})
    else:
        messages.error(request, 'no existen cargos disponibles')
        return redirect('fichaCargo')


# creacion de liquidaciones
def crear_liquidacion(request):
    if request.method == 'post':
        rut = request.post.get('rut')
        mes_liquidacion = request.post.get('mes_liquidacion')
        archivo_liquidacion = request.post.get('archivo_liquidacion')

        try:
            trabajador = Trabajador.objects.get(rut=rut)
            formulario = Liquidacion(rut=trabajador, mes_liquidacion=mes_liquidacion, archivo_liquidacion=archivo_liquidacion)
            formulario.save()
            messages.success(request, 'creación exitosa')
            return redirect('liquidacion')


        except Exception as e:
            messages.error(request, 'no existen liquidaciones disponibles')
            return render(request, 'RRHH/crear_liquidacion.html')

    trabajadores = Trabajador.objects.all()

    if trabajadores:
        return render(request, 'RRHH/crear_liquidacion.html', {'trabajadores':trabajadores})

    else:
        messages.error(request, 'no existen rut disponibles')
        return redirect('liquidacion')


# ver liquidaciones
class Ver_liquidacion(ListView):
    model = Liquidacion
    template_name = 'RRHH/ver_ficha_liquidaciones.html'
    def get_queryset(self):
        liquidaciones = Liquidacion.objects.all()
        return liquidaciones

    def get_context_data(self, **kwargs) :
        context =  super().get_context_data(**kwargs)
        context ['tittle'] = 'verliquidacion'
        context ['liquidaciones'] = self.get_queryset()
        return context

# creacion de registro médico
def crear_registro_medico(request):
    if request.method == 'post':
        rut = request.post.get('rut')
        tipo_registro = request.post.get('tipo_registro')
        rm_fecha_ingreso = request.post.get('rm_fecha_ingreso')
        rm_fecha_termino = request.post.get('rm_fecha_termino')
        archivo_medico = request.post.get('archivo_medico')

        try:
            trabajador = Trabajador.objects.get(rut=rut)
            formulario = RegistroMedico(rut=trabajador, tipo_registro=tipo_registro, rm_fecha_ingreso=rm_fecha_ingreso, rm_fecha_termino=rm_fecha_termino, archivo_medico=archivo_medico)
            formulario.save()
            messages.success(request, 'creación exitosa')
            return redirect('registro_medico')


        except Exception as e:
            messages.error(request, 'no existen registro médicos disponibles')
            return render(request, 'RRHH/crear_registro_medico.html')

    trabajadores = Trabajador.objects.all()

    if trabajadores:
        return render(request, 'RRHH/crear_registro_medico.html', {'trabajadores':trabajadores})

    else:
        messages.error(request, 'no existen rut disponibles')
        return redirect('registro_medico')


# ver registro médico
class Ver_registro_medico(ListView):
    model = RegistroMedico
    template_name = 'RRHH/ver_registro_medico.html'
    def get_queryset(self):
        registros_medicos = RegistroMedico.objects.all()
        return registros_medicos

    def get_context_data(self, **kwargs) :
        context =  super().get_context_data(**kwargs)
        context ['tittle'] = 'verregistromedico'
        context ['registros_medicos'] = self.get_queryset()
        return context