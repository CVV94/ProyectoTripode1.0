from django.urls import path
from appDb import views
from django.contrib.auth import views as auth_views


# from django.views.generic import TemplateView

urlpatterns = [
    path('', views.index, name='index'),
    path('perfil/', views.crear_perfil, name='perfil'),
    path('home/', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('registrarse/', views.registrarse, name='registro'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

]

    # path('listadoJson/', views.listado_trabajadores, name='listadoJason'),