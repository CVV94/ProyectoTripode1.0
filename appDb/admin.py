from django.contrib import admin
from .models import Perfil
from .models import Usuario
from .models import Trabajador
from .models import Area
from .models import Departamento
from .models import Cargo

# Register your models here.

admin.site.register(Perfil)
admin.site.register(Usuario)
admin.site.register(Trabajador)
admin.site.register(Area)
admin.site.register(Departamento)
admin.site.register(Cargo)
