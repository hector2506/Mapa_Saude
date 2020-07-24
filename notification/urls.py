from django.contrib import admin
from django.urls import path,include
from .views import *
from django.contrib.auth import views as auth_views

app_name = "notification"

urlpatterns = [
    path('lista_notificacao/',notificacao_list, name='notificacao_list'),
    path('novo_notificacao/',novo_notificacao, name='novo_notificacao'),
]