from django.shortcuts import render,redirect
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required  
from django.contrib import messages
from django.urls import reverse_lazy   #importacion para redireccionamientos de django con clases
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
    return render(request,'RRHH/moduloRRHH.html') # Redireccionar a la página del módulo de RRHH.


def moduloJefeRRHH(request):
    return render(request,'RRHH/moduloJefeRRHH.html') # Redireccionar a la página del módulo de Jefe de RRHH.


def moduloTrabajador(request):
    return render(request,'RRHH/moduloTrabajador.html') # Redireccionar a la página del módulo de Trabajador

def prueba(request):
    return render(request,'RRHH/prueba.html')


login_required
class ListadoTrabajador(ListView):
    model = Trabajador                                  #Modelo con el que trabaja
    template_name = 'RRHH/trabajadores.html'         #direccion template
    
    def get_queryset(self):                             #Consultas de ORM
        trabajadores = Trabajador.objects.select_related('id_cargo').values('rut', 'nombre', 'sexo', 'id_cargo__nombre_cargo')
        return trabajadores
    
    def get_context_data(self, **kwargs):             #pasa un contexto de las consultas a la planilla html{{}}  
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Trabajadores'
        context['trabajadores'] = self.get_queryset()
        return context
    
    
    

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
            return redirect('fichaTrabajador')  # Redireccionar a la misma página después de guardar
        except Exception as e:
            messages.error(request, 'Ocurrió un error al crear la ficha del trabajador: {}'.format(str(e)))
            return redirect('fichaTrabajador')  # Redireccionar a la misma página si ocurre una excepción
    
    cargos = Cargo.objects.all()
    usuarios = Usuario.objects.all()
    
    if cargos.exists() and usuarios.exists():  # Usar 'and' en lugar de 'or'
        return render(request, 'RRHH/fichaTrabajador.html', {'cargos': cargos, 'usuarios': usuarios})
    else:
        messages.error(request, 'No existen cargos y usuarios disponibles')
        return redirect('fichaTrabajador')
    
def fichaArea(request):
    if request.method == 'POST':
        id_area = request.POST.get('id_area')
        nombre_area = request.POST.get('nombre_area')
        try:
            area = Area(id_area=id_area, nombre_area=nombre_area)
            area.save()
            return redirect('fichaDepartamento') # Redireccionar con el argumento id_area
        except Exception as e:
            messages.error(request, 'Ocurrió un error al crear el área: {}'.format(str(e)))
            return render(request, 'RRHH/fichaArea.html')
    return render(request, 'RRHH/fichaArea.html')

def fichaDepartamento(request):
    if request.method == 'POST':
        id_departamento = request.POST.get('id_departamento')
        id_area = request.POST.get('id_area')  # Corregir el nombre del campo a 'id_area'
        departamento = request.POST.get('departamento')
        try:
            area = Area.objects.get(id_area=id_area)
            departamento = Departamento(id_departamento=id_departamento, id_area=area, departamento=departamento)  # Usar 'id_area' en lugar de 'area'
            departamento.save()
            messages.success(request, 'Departamento creado exitosamente.')
            return redirect('fichaCargo')
        except Exception as e:
            messages.error(request, 'Ocurrió un error al crear el departamento: {}'.format(str(e)))
            return render(request, 'RRHH/fichaDepartamento.html')
    
    areas = Area.objects.all()
    if areas:
        return render(request, 'RRHH/fichaDepartamento.html', {'areas': areas})
    else:
        messages.error(request, 'No existen áreas disponibles')
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
            messages.success(request, 'Cargo creado exitosamente.')
            return redirect('fichaTrabajador')
        except Exception as e:
            messages.error(request, 'Ocurrió un error al crear el cargo: {}'.format(str(e)))
            return render(request, 'RRHH/fichaCargo.html')
    departamentos = Departamento.objects.all()

    if departamentos:
        return render(request, 'RRHH/fichaCargo.html', {'departamentos': departamentos})
    else:
        messages.error(request, 'No existen Cargos disponibles')
        return redirect('fichaCargo')
    
class GestionSolicitud(CreateView):
    model = VacacionLicencia
    form_class= LicenciaForm
    template_name = 'RRHH/gestionSolicitud.html'
    # success_url= reverse_lazy('RecursosHumanos:fichaCargo')

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['title'] = 'Gestion de Solicitudes'
        return context
    



# Creacion de liquidaciones
def crear_liquidacion(request):
    if request.method == 'POST':
        rut = request.POST.get('rut')
        mes_liquidacion = request.POST.get('mes_liquidacion')
        archivo_liquidacion = request.POST.get('archivo_liquidacion')
        
        try:
            trabajador = Trabajador.objects.get(rut=rut)
            formulario = Liquidacion(rut=trabajador, mes_liquidacion=mes_liquidacion, archivo_liquidacion=archivo_liquidacion)
            formulario.save()
            messages.success(request, 'Creación exitosa')
            return redirect('liquidacion')
        

        except Exception as e:
            messages.error(request, 'No existen liquidaciones disponibles')
            return render(request, 'RRHH/crear_liquidacion.html')
    
    trabajadores = Trabajador.objects.all()

    if trabajadores:
        return render(request, 'RRHH/crear_liquidacion.html', {'trabajadores':trabajadores})
    
    else:
        messages.error(request, 'No existen rut disponibles')
        return redirect('liquidacion')


# Ver liquidaciones
class Ver_liquidacion(ListView):
    model = Liquidacion 
    template_name = 'RRHH/ver_ficha_liquidaciones.html'
    def get_queryset(self):
        liquidaciones = Liquidacion.objects.all()
        return liquidaciones
    
    def get_context_data(self, **kwargs) :
        context =  super().get_context_data(**kwargs)
        context ['tittle'] = 'VerLiquidacion'
        context ['liquidaciones'] = self.get_queryset()
        return context
    




# Creacion de registro médico
def crear_registro_medico(request):
    if request.method == 'POST':
        rut = request.POST.get('rut')
        tipo_registro = request.POST.get('tipo_registro')
        rm_fecha_ingreso = request.POST.get('rm_fecha_ingreso')
        rm_fecha_termino = request.POST.get('rm_fecha_termino')
        archivo_medico = request.POST.get('archivo_medico')
        
        try:
            trabajador = Trabajador.objects.get(rut=rut)
            formulario = RegistroMedico(rut=trabajador, tipo_registro=tipo_registro, rm_fecha_ingreso=rm_fecha_ingreso, rm_fecha_termino=rm_fecha_termino, archivo_medico=archivo_medico)
            formulario.save()
            messages.success(request, 'Creación exitosa')
            return redirect('registro_medico')
        

        except Exception as e:
            messages.error(request, 'No existen registro médicos disponibles')
            return render(request, 'RRHH/crear_registro_medico.html')
    
    trabajadores = Trabajador.objects.all()

    if trabajadores:
        return render(request, 'RRHH/crear_registro_medico.html', {'trabajadores':trabajadores})
    
    else:
        messages.error(request, 'No existen rut disponibles')
        return redirect('registro_medico')


# Ver Registro médico
class Ver_registro_medico(ListView):
    model = RegistroMedico
    template_name = 'RRHH/ver_registro_medico.html'
    def get_queryset(self):
        registros_medicos = RegistroMedico.objects.all()
        return registros_medicos
    
    def get_context_data(self, **kwargs) :
        context =  super().get_context_data(**kwargs)
        context ['tittle'] = 'VerRegistroMedico'
        context ['registros_medicos'] = self.get_queryset()
        return context