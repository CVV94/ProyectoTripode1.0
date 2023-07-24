# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Area(models.Model):
    id_area = models.AutoField(db_column='ID_AREA', primary_key=True)  # Field name made lowercase.
    nombre_area = models.CharField(db_column='NOMBRE_AREA', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'area'
    def __str__(self) -> str:
        return self.nombre_area


class AtorizacionPermiso(models.Model):
    id_autorizacion = models.AutoField(db_column='ID_AUTORIZACION', primary_key=True)  # Field name made lowercase.
    rut = models.ForeignKey('Trabajador', models.DO_NOTHING, db_column='RUT')  # Field name made lowercase.
    vehiculo = models.CharField(db_column='VEHICULO', max_length=50)  # Field name made lowercase.
    autorizacion_inicio = models.DateField(db_column='AUTORIZACION_INICIO')  # Field name made lowercase.
    autorizacion_fin = models.DateField(db_column='AUTORIZACION_FIN')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'atorizacion_permiso'
    def __str__(self) -> str:
        return self.rut


class CargaFamiliar(models.Model):
    id_carga_familiar = models.AutoField(db_column='ID_CARGA_FAMILIAR', primary_key=True)  # Field name made lowercase.
    rut = models.ForeignKey('Trabajador', models.DO_NOTHING, db_column='RUT')  # Field name made lowercase.
    cf_nombre = models.CharField(db_column='CF_NOMBRE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    parentesco = models.CharField(db_column='PARENTESCO', max_length=40, blank=True, null=True)  # Field name made lowercase.
    cf_sexo = models.CharField(db_column='CF_SEXO', max_length=9, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'carga_familiar'
    def __str__(self) -> str:
        return self.cf_nombre, self.parentesco, self.cf_sexo 


class Cargo(models.Model):
    id_cargo = models.AutoField(db_column='ID_CARGO', primary_key=True)  # Field name made lowercase.
    id_departamento = models.ForeignKey('Departamento', models.DO_NOTHING, db_column='ID_DEPARTAMENTO')  # Field name made lowercase.
    nombre_cargo = models.CharField(db_column='NOMBRE_CARGO', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'cargo'
    def __str__(self) -> str:
        return f'{self.id_cargo} "{self.id_departamento}"  "{self.nombre_cargo}" '


class ContactoEmergencia(models.Model):
    id_emergencia = models.AutoField(db_column='ID_EMERGENCIA', primary_key=True)  # Field name made lowercase.
    rut = models.ForeignKey('Trabajador', models.DO_NOTHING, db_column='RUT')  # Field name made lowercase.
    ce_nombre = models.CharField(db_column='CE_NOMBRE', max_length=50)  # Field name made lowercase.
    relacion_con_trabajador = models.CharField(db_column='RELACION_CON_TRABAJADOR', max_length=40)  # Field name made lowercase.
    ce_telefono = models.IntegerField(db_column='CE_TELEFONO')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'contacto_emergencia'


class Contrato(models.Model):
    id_contrato = models.AutoField(db_column='ID_CONTRATO', primary_key=True)  # Field name made lowercase.
    rut = models.ForeignKey('Trabajador', models.DO_NOTHING, db_column='RUT')  # Field name made lowercase.
    tipo_contrato = models.CharField(db_column='TIPO_CONTRATO', max_length=40)  # Field name made lowercase.
    contrato_inicio = models.DateField(db_column='CONTRATO_INICIO')  # Field name made lowercase.
    contrato_termino = models.DateField(db_column='CONTRATO_TERMINO')  # Field name made lowercase.
    archivo_contrato = models.TextField(db_column='ARCHIVO_CONTRATO')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'contrato'


class Departamento(models.Model):
    id_departamento = models.AutoField(db_column='ID_DEPARTAMENTO', primary_key=True)  # Field name made lowercase.
    id_area = models.ForeignKey(Area, models.DO_NOTHING, db_column='ID_AREA')  # Field name made lowercase.
    departamento = models.CharField(db_column='DEPARTAMENTO', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'departamento'


class EvaluacionDesempeno(models.Model):
    id_evaluacion = models.AutoField(db_column='ID_EVALUACION', primary_key=True)  # Field name made lowercase.
    rut = models.ForeignKey('Trabajador', models.DO_NOTHING, db_column='RUT')  # Field name made lowercase.
    tipo_evaluacion = models.CharField(db_column='TIPO_EVALUACION', max_length=50)  # Field name made lowercase.
    calificacion = models.IntegerField(db_column='CALIFICACION')  # Field name made lowercase.
    fecha_evaluacion = models.DateField(db_column='FECHA_EVALUACION')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'evaluacion_desempeno'


class Liquidacion(models.Model):
    id_liquidacion = models.AutoField(db_column='ID_LIQUIDACION', primary_key=True)  # Field name made lowercase.
    rut = models.ForeignKey('Trabajador', models.DO_NOTHING, db_column='RUT')  # Field name made lowercase.
    mes_liquidacion = models.DateField(db_column='MES_LIQUIDACION', blank=True, null=True)  # Field name made lowercase.
    archivo_liquidacion = models.TextField(db_column='ARCHIVO_LIQUIDACION', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'liquidacion'


class Perfil(models.Model):
    id_perfil = models.AutoField(db_column='ID_PERFIL', primary_key=True)  # Field name made lowercase.
    nombre_perfil = models.CharField(db_column='NOMBRE_PERFIL', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'perfil'

    def __str__(self):
        return self.nombre_perfil




class RegistroMedico(models.Model):
    id_registro_medico = models.AutoField(db_column='ID_REGISTRO_MEDICO', primary_key=True)  # Field name made lowercase.
    rut = models.ForeignKey('Trabajador', models.DO_NOTHING, db_column='RUT')  # Field name made lowercase.
    tipo_registro_medico = models.CharField(db_column='TIPO_REGISTRO_MEDICO', max_length=50)  # Field name made lowercase.
    rm_fecha_ingreso = models.DateField(db_column='RM_FECHA_INGRESO')  # Field name made lowercase.
    rm_fecha_termino = models.DateField(db_column='RM_FECHA_TERMINO')  # Field name made lowercase.
    archivo_medico = models.TextField(db_column='ARCHIVO_MEDICO')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'registro_medico'


class Trabajador(models.Model):
    rut = models.CharField(db_column='RUT', primary_key=True, max_length=16)  # Field name made lowercase.
    id_cargo = models.ForeignKey(Cargo, models.DO_NOTHING, db_column='ID_CARGO')  # Field name made lowercase.
    id_usuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='ID_USUARIO')  # Field name made lowercase.
    nombre = models.CharField(db_column='NOMBRE', max_length=50)  # Field name made lowercase.
    sexo = models.CharField(db_column='SEXO', max_length=9)  # Field name made lowercase.
    direccion = models.CharField(db_column='DIRECCION', max_length=50)  # Field name made lowercase.
    telefono = models.IntegerField(db_column='TELEFONO')  # Field name made lowercase.
    fecha_ingreso = models.DateField(db_column='FECHA_INGRESO')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'trabajador'
    def __str__(self):
        return f'{self.rut}'


class Usuario(models.Model):
    id_usuario = models.AutoField(db_column='ID_USUARIO', primary_key=True)  # Field name made lowercase.
    id_perfil = models.ForeignKey(Perfil, models.DO_NOTHING, db_column='ID_PERFIL')  # Field name made lowercase.
    nombre_usuario = models.CharField(db_column='NOMBRE_USUARIO', max_length=50)  # Field name made lowercase.
    password = models.CharField(db_column='PASSWORD', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'usuario'
    def __str__(self):
        return f"Id_Usuario :{str(self.id_usuario)} --Id_Perfil:{str(self.id_perfil)}--Nombre:{self.nombre_usuario} --Password: {self.password}"


class VacacionLicencia(models.Model):
    id_solicitud = models.AutoField(db_column='ID_SOLICITUD', primary_key=True)  # Field name made lowercase.
    rut = models.ForeignKey(Trabajador, models.DO_NOTHING, db_column='RUT')  # Field name made lowercase.
    tipo_solicitud = models.CharField(db_column='TIPO_SOLICITUD', max_length=10)  # Field name made lowercase.
    fecha_inicio = models.DateField(db_column='FECHA_INICIO')  # Field name made lowercase.
    fecha_fin = models.DateField(db_column='FECHA_FIN')  # Field name made lowercase.
    dias = models.IntegerField(db_column='DIAS')  # Field name made lowercase.
    estado = models.CharField(db_column='ESTADO', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'vacacion_licencia'
    def __str__(self):
        return f'{self.rut}'