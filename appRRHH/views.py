from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy   # importacion para redireccionamientos de django con clases
from django.views.generic import CreateView
from django.views.generic.edit import UpdateView
from appRRHH.forms import LicenciaForm
from appDb.models import Trabajador
from appDb.models import Cargo
from appDb.models import Usuario
from appDb.models import Departamento
from appDb.models import Area
from appDb.models import VacacionLicencia
from appDb.models import Liquidacion
from appDb.models import RegistroMedico
from appDb.models import EvaluacionDesempeno

def moduloRRHH(request):
    return render(request, 'RRHH/moduloRRHH.html')  # redireccionar a la página del módulo de rrhh.


def moduloJefeRRHH(request):
    return render(request,'RRHH/moduloJefeRRHH.html') # redireccionar a la página del módulo de jefe de rrhh.


def moduloTrabajador(request):
    return render(request,'RRHH/moduloRRHH.html') # redireccionar a la página del módulo de trabajador

def tipoDeSolicitudes(request):
    return render(request,'RRHH/tipodeSolicitudes.html' )

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
        solicitudes = VacacionLicencia.objects.filter(estado='Pendiente')
        return solicitudes

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'listado de Solicitudes Pendientes'
        context["solicitudes"] = self.get_queryset()
        return context

class SolicitudesGestionadas(ListView):
    model = VacacionLicencia
    template_name = 'RRHH/solicitudesGestionadas.html'
    def dispatch(self, request, *args, **kwargs):           # Se usa para redireccionar
        return super().dispatch(request, *args, **kwargs)
    def get_queryset(self):
        solicitudes = VacacionLicencia.objects.exclude(estado='Pendiente')
        return solicitudes

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'listado de Solicitudes Gestionadas'
        context["solicitudes"] = self.get_queryset()
        return context



class GestionSolicitud(CreateView):
    model = VacacionLicencia
    form_class= LicenciaForm
    template_name = 'RRHH/gestionSolicitud.html'
    success_url = reverse_lazy('listSolicitudes')

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['title'] = 'gestion de solicitudes'
        return context

class EditSolicitud(UpdateView):
    model = VacacionLicencia
    form_class = LicenciaForm
    template_name = 'RRHH/edit_solicitud.html'
    success_url = reverse_lazy('listSolicitudes')


def fichaTrabajador(request):
    if request.method == 'POST':
        rut = request.POST.get('rut')
        nombre = request.POST.get('nombre')
        sexo = request.POST.get('sexo')
        direccion = request.POST.get('direccion')
        telefono = request.POST.get('telefono')
        fecha_ingreso = request.POST.get('fecha_ingreso')
        id_cargo = request.POST.get('id_cargo')
        id_usuario = request.POST.get('id_usuario')

        try:
            cargo = Cargo.objects.get(id_cargo=id_cargo)
            usuario = Usuario.objects.get(id_usuario=id_usuario)
            trabajador = Trabajador(rut=rut, nombre=nombre, sexo=sexo, direccion=direccion, telefono=telefono, fecha_ingreso=fecha_ingreso, id_cargo=cargo, id_usuario=usuario)
            trabajador.save()
            return redirect('fichaTrabajador')  # redireccionar a la misma página después de guardar
        except Exception as e:
            messages.error(request, 'ocurrió un error al crear la ficha del trabajador: {}'.format(str(e)))
            return redirect('fichaTrabajador')  # redireccionar a la misma página si ocurre una excepción

    cargos = Cargo.objects.all()
    usuarios = Usuario.objects.all()

    if cargos.exists() and usuarios.exists():  # usar 'and' en lugar de 'or'
        return render(request, 'RRHH/fichaTrabajador.html', {'cargos': cargos, 'usuarios': usuarios})
    else:
        messages.error(request, 'no existen cargos y usuarios disponibles')
        return redirect('fichaTrabajador')

def fichaArea(request):
    if request.method == 'POST':
        id_area = request.POST.get('id_area')
        nombre_area = request.POST.get('nombre_area')
        try:
            area = Area(id_area=id_area, nombre_area=nombre_area)
            area.save()
            return redirect('fichaDepartamento') # redireccionar con el argumento id_area
        except Exception as e:
            messages.error(request, 'ocurrió un error al crear el área: {}'.format(str(e)))
            return render(request, 'RRHH/fichaArea.html')
    return render(request, 'RRHH/fichaArea.html')

def fichaDepartamento(request):
    if request.method == 'POST':
        id_departamento = request.POST.get('id_departamento')
        id_area = request.POST.get('id_area')  # corregir el nombre del campo a 'id_area'
        departamento = request.POST.get('departamento')
        try:
            area = Area.objects.get(id_area=id_area)
            departamento = Departamento(id_departamento=id_departamento, id_area=area, departamento=departamento)  # usar 'id_area' en lugar de 'area'
            departamento.save()
            messages.success(request, 'departamento creado exitosamente.')
            return redirect('fichaCargo')
        except Exception as e:
            messages.error(request, 'ocurrió un error al crear el departamento: {}'.format(str(e)))
            return render(request, 'RRHH/fichaDepartamento.html')

    areas = Area.objects.all()
    if areas:
        return render(request, 'RRHH/fichaDepartamento.html', {'areas': areas})
    else:
        messages.error(request, 'no existen áreas disponibles')
        return redirect('fichaDepartamento')

def fichaCargo(request):
    if request.method == 'POST':
        id_cargo=request.POST.get('id_cargo')
        id_departamento=request.POST.get('id_departamento')
        nombre_cargo=request.POST.get('nombre_cargo')
        try:
            departamento=Departamento.objects.get(id_departamento=id_departamento)
            cargo=Cargo(id_cargo=id_cargo,id_departamento=departamento,nombre_cargo=nombre_cargo)
            cargo.save()
            messages.success(request, 'cargo creado exitosamente.')
            return redirect('fichaTrabajador')
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
    if request.method == 'POST':
        rut = request.POST.get('rut')
        mes_liquidacion = request.POST.get('mes_liquidacion')
        archivo_liquidacion = request.POST.get('archivo_liquidacion')

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
    if request.method == 'POST':
        rut = request.POST.get('rut')
        tipo_registro_medico = request.POST.get('tipo_registro_medico')
        rm_fecha_ingreso = request.POST.get('rm_fecha_ingreso')
        rm_fecha_termino = request.POST.get('rm_fecha_termino')
        archivo_medico = request.POST.get('archivo_medico')

        try:
            trabajador = Trabajador.objects.get(rut=rut)
            formulario = RegistroMedico(rut=trabajador, tipo_registro_medico=tipo_registro_medico, rm_fecha_ingreso=rm_fecha_ingreso, rm_fecha_termino=rm_fecha_termino, archivo_medico=archivo_medico)
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




# Creacion evaluacion
def crear_evaluacion(request):
    if request.method == 'POST':
        rut = request.POST.get('rut')
        tipo_evaluacion = request.POST.get('tipo_evaluacion')
        calificacion = request.POST.get('calificacion')
        fecha_evaluacion = request.POST.get('fecha_evaluacion')

        try:
            trabajador = Trabajador.objects.get(rut=rut)
            formulario = EvaluacionDesempeno(rut=trabajador, tipo_evaluacion=tipo_evaluacion, calificacion=calificacion, fecha_evaluacion=fecha_evaluacion)
            formulario.save()
            messages.success(request, 'Creación exitosa')
            return redirect('evaluacion')
        

        except Exception as e:
            messages.error(request, 'No existen evaluaciones disponibles')
            return render(request, 'RRHH/crear_evaluacion.html')
    
    trabajadores = Trabajador.objects.all()

    if trabajadores:
        return render(request, 'RRHH/crear_evaluacion.html', {'trabajadores':trabajadores})
    
    else:
        messages.error(request, 'No existen rut disponibles')
        return redirect('evaluacion')
    

# Ver Evaluación
class Ver_evaluacion(ListView):
    model = EvaluacionDesempeno
    template_name = 'RRHH/ver_evaluacion.html'
    def get_queryset(self):
        evaluaciones = EvaluacionDesempeno.objects.all()
        return evaluaciones
    
    def get_context_data(self, **kwargs) :
        context =  super().get_context_data(**kwargs)
        context ['tittle'] = 'VerEvaluaciones'
        context ['evaluaciones'] = self.get_queryset()
        return context
    



# Ver listado filtrado
def filtro_trabajadores(request):
    # Obtener los valores únicos de sexo, cargo, área y departamento para los filtros
    sexos = Trabajador.objects.values_list('sexo', flat=True).distinct()
    nombre_cargos = Cargo.objects.all()
    departamentos = Departamento.objects.all()
    nombre_areas = Area.objects.all()

    # Obtener los parámetros de filtrado enviados por el formulario
    filtro_sexo = request.GET.get('sexo')
    filtro_cargo = request.GET.get('nombre_cargo')
    filtro_departamento = request.GET.get('departamento')
    filtro_area = request.GET.get('nombre_area')
    

    # Realizar la consulta para filtrar los trabajadores según los parámetros recibidos
    trabajadores_filtrados = Trabajador.objects.filter(sexo=filtro_sexo)

    if filtro_cargo:
        trabajadores_filtrados = trabajadores_filtrados.filter(nombre_cargo__nombre_cargo=filtro_cargo)

    if filtro_area:
        trabajadores_filtrados = trabajadores_filtrados.filter(nombre_cargo__departamento__area__nombre_area=filtro_area)

    if filtro_departamento:
        trabajadores_filtrados = trabajadores_filtrados.filter(nombre_cargo__departamento__departamento=filtro_departamento)

    # Renderizar el template de resultados de búsqueda y pasar los trabajadores filtrados y los filtros disponibles
    return render(request, 'RRHH/filtro_trabajadores.html', {
        'trabajadores_filtrados': trabajadores_filtrados,
        'sexo': sexos,
        'cargos': nombre_cargos,
        'areas': nombre_areas,
        'departamentos': departamentos,
        'filtro_sexo': filtro_sexo,
        'filtro_cargo': filtro_cargo,
        'filtro_area': filtro_area,
        'filtro_departamento': filtro_departamento,
    })