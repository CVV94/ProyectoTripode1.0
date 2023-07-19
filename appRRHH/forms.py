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
            'fecha_inicio': DateInput(attrs={'type': 'date'}),
            'fecha_fin': DateInput(attrs={'type': 'date'}),
            'estado': TextInput(attrs={'type': 'text'}),

        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)               #self.instance.pk  sirve para objetos creados al inicio
        if not self.instance.pk:                        #Solo cuando se crea la solicitud su estado sera por defecto "En Proceso"
            self.fields['estado'].initial="En Proceso"