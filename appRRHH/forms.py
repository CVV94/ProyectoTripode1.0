from django.forms import *
from appDb.models import VacacionLicencia

class LicenciaForm(ModelForm):
    class Meta:
        model = VacacionLicencia
        fields= '__all__'
        labels = {
            'rut': 'Rut',
            'tipo_solicitud': 'Tipo de Solicitud',
            'fecha_inicio': 'Fecha de Inicio',
        }
        widgets = {
            'fecha_inicio': DateInput(attrs={'type': 'date'})
        }