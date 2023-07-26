from django.forms import *
from appDb.models import VacacionLicencia


class LicenciaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            html_id = f"id_{field_name}"  # Genera el id para el campo actual (por ejemplo, 'id_rut', 'id_tipo_solicitud', etc.)
            field.widget.attrs['id'] = html_id

    class Meta:
        model = VacacionLicencia
        fields = '__all__'
        labels = {
            'rut': 'Rut',
            'tipo_solicitud': 'Tipo de Solicitud',
            'fecha_inicio': 'Fecha de inicio',
            # Agrega los demás campos y sus etiquetas aquí
        }
        widgets = {
            'fecha_inicio': DateInput(attrs={'type': 'date'}),
            'fecha_fin': DateInput(attrs={'type': 'date'}),
            'estado': TextInput(attrs={'type': 'text'}),
            # Agrega los widgets para los demás campos aquí
        }