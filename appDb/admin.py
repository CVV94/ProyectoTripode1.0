from django.contrib import admin
from .models import Perfil
from .models import Usuario
from .models import Trabajador
from .models import Area
from .models import Departamento
from .models import Cargo
from .models import Liquidacion
from .models import CargaFamiliar
from .models import ContactoEmergencia
from .models import RegistroMedico
from .models import VacacionLicencia
from .models import EvaluacionDesempeno
from .models import AtorizacionPermiso
from .models import Contrato




# Register your models here.

admin.site.register(Perfil)
admin.site.register(Usuario)
admin.site.register(Trabajador)
admin.site.register(Area)
admin.site.register(Departamento)
admin.site.register(Cargo)
admin.site.register(CargaFamiliar)
admin.site.register(ContactoEmergencia)
admin.site.register(RegistroMedico)
admin.site.register(VacacionLicencia)
admin.site.register(EvaluacionDesempeno)
admin.site.register(AtorizacionPermiso)
admin.site.register(Contrato)
admin.site.register(Liquidacion)
