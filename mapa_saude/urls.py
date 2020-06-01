from django.contrib import admin
from django.urls import path
from site_mapa.views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',paciente_list, name='home'),
    path('login/',login_view, name='login'),
    path('register/',register_view, name='register'),
    path('logout/',logout_view, name='logout'),
    path('lista_notificacao/',notificacao_list, name='notificacao_list'),
    path('novo_paciente/',novo_paciente, name='novo_paciente'),
    path('novo_notificacao/',novo_notificacao, name='novo_notificacao'),
    path('mapa/',mapa, name='mapa'),
]
